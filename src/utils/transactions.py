"""
Persistence of all transactions to the database are carried out of this module.

"""

import time

from src import db
from src.helpers.references import References
# from ..cob.log_module import SystemOBS
from ..functions.Enums import TransactionType, TransactionMethod, AccountTypes
from ..functions.genarators import Auto, Getters
from ..models.customer_model import Customer
from ..models.till_model import Till
from ..models.transaction_base_model import TransactionBase
from ..models.transaction_charge_fee_model import TransactionChargeFee
from ..models.transaction_fee_charge_table_model import TransactionFeeChargeTable
from ..models.transaction_model import Transaction


# from src.models import session


# class Transaction(object):
#     """
#     main transaction class. every transaction has a date amount and credit account
#
#     """
#
#     def __init__(self, date, amount, cr_account):
#         self.date = date
#         self.amount = float(amount)
#         self.cr_account = cr_account
#
#     def __str__(self):
#         return self.cr_account

# @property
# def amount(self):
#     return float(self.amount)
#
# @amount.setter
# def amount(self, value):
#     self.amount = value


class CommitTransaction:
    """
    This class handles the commission of transaction in the database. all parameters have to be
    supplies in order for the record to be committed to the Transaction table.
    """

    def __init__(self, trans_type,
                 trans_ref,
                 trans_method,
                 dr_account_number,
                 cr_account_number,
                 amount,
                 current_balance,
                 remark,
                 customer_id,
                 cheque_number='',
                 trans_date=time.strftime('%Y-%m-%d')
                 ):
        self.trans_type = trans_type
        self.trans_ref = trans_ref
        self.trans_method = trans_method
        self.trans_date = trans_date
        self.cheque_number = cheque_number
        self.dr_account_number = dr_account_number
        self.cr_account_number = cr_account_number
        self.amount = amount
        self.current_balance = current_balance
        self.remark = remark
        self.customer_id = customer_id

    def __str__(self):
        return self.dr_account_number

    def commit_to_database(self):
        """
        persists a transaction record in the database using the session instance.
        :return:
        """
        transaction = Transaction(trantype=self.trans_type,
                                  tranref=self.trans_ref,
                                  tranmethod=self.trans_method,
                                  tran_date=self.trans_date,
                                  cheque_num=self.cheque_number,
                                  acc_number=self.dr_account_number,
                                  cr_acc_number=self.cr_account_number,
                                  amount=self.amount,
                                  current_balance=self.current_balance,
                                  remark=self.remark,
                                  custid=self.customer_id)
        db.session.add(transaction)
        db.session.commit()


class AccountTransaction(Transaction):
    """
    This class handles customer account transaction of different types which include account
    creation, Withdrawals, Deposits, Transfers

    todo: Change class name to ProcessAccountTransaction
    """

    def __init__(self, date, amount, cr_account):
        TransactionBase.__init__(self, date, amount, cr_account)
        self.suspense_account_new_account = db.session.query(Customer).filter_by(
            account_type=AccountTypes.ACCOUNT_CREATION.value).first()
        if Getters.get_till_details() is not None:
            self.suspense_account_teller = db.session.query(Till).filter_by(
                till_account=Getters.get_till_details().till_account).first()
        else:
            # SystemOBS.start_logging("there are no till details")
            "None"

        self.suspense_account_charges = db.session \
            .query(Customer) \
            .filter_by(account_type=AccountTypes.CHARGES.value).first()

    def create_account(self):

        """
        this method does not take any parameter. it creates a new account and associates it to the
        customer ID for the new customer created
        :return: 0 for exception, 1 for account created
        """
        # suspense_account = session.query(Customer).filter_by(account_type='acccreate').first()
        try:
            customer = db.session.query(Customer).filter_by(acc_number=self.cr_account).one()
        except ValueError as value_error:
            print(value_error)
            # SystemOBS().start_logging(value_error)
            return 0
        # Update transactions Table
        CommitTransaction(trans_type=TransactionType.CREDIT.value,
                          trans_ref=References().get_transaction_reference,
                          trans_method=TransactionMethod.CASH.value,
                          cheque_number='None',
                          dr_account_number=self.suspense_account_new_account.acc_number,
                          cr_account_number=self.cr_account,
                          amount=self.amount,
                          current_balance=round(self.amount, 2),
                          remark='Account Creation',
                          customer_id=customer.custid) \
            .commit_to_database()

        # update the Account creation Suspense Account
        self.suspense_account_new_account.working_bal -= self.amount
        db.session.add(self.suspense_account_new_account)
        db.session.commit()
        # SystemOBS.start_logging("Account Created: " + str(customer.acc_number))
        return 1
        # ---------------------------------------------

    def deposit(self, transaction_reference):
        """
        This method takes an additional parameter @transaction_reference for a deposit transaction
        to be saved in the database.
            - A deposit affects the Teller Till account, this means theTeller Account is debited
            and Customer account credited.
        """
        customer = db.session.query(Customer).filter_by(acc_number=self.cr_account).one()
        current_balance = float(self.amount) + float(customer.working_bal)
        trans_ref = References().get_transaction_reference

        CommitTransaction(trans_type=TransactionType.CREDIT.value,
                          trans_ref=trans_ref,
                          trans_method=TransactionMethod.CASH.value,
                          trans_date=self.date,
                          cheque_number='None',
                          dr_account_number=self.suspense_account_teller.till_account,
                          cr_account_number=self.cr_account,
                          amount=self.amount,
                          current_balance=round(current_balance, 2),
                          remark='Deposit_' + transaction_reference,
                          customer_id=customer.custid).commit_to_database()

        # Update customers working balance
        customer.working_bal = round(current_balance, 2)
        db.session.add(customer)
        db.session.commit()
        # -------------------------------

        # Update Till Opening/Closing   Balance
        self.suspense_account_teller.c_balance -= round(float(self.amount), 2)
        db.session.add(self.suspense_account_teller)
        db.session.commit()

    def withdrawal(self, transaction_reference):
        """
        This method takes in transaction reference generated at the point of withdrawal and save
        the record in the Transaction table. in a withdrawal, two transaction record are created,
        one for the debited account and the other for the credited account.

            - A withdrawal affects the Tellers till balance, this means the Teller account will be
            credited and customer account debited """
        customer = db.session.query(Customer).filter_by(acc_number=self.cr_account).one()

        current_balance = float(customer.working_bal) - float(self.amount)
        main_withdrawal_transaction \
            = Transaction(trantype='DR',
                          tranref=transaction_reference,
                          tranmethod='Cash',
                          tran_date=self.date,
                          cheque_num='None',
                          acc_number=int(self.cr_account),
                          cr_acc_number=int(self.suspense_account_teller.till_account),
                          amount=self.amount,
                          current_balance=round(current_balance, 2),
                          remark='Withdrawal ' + transaction_reference,
                          custid=customer.custid)
        db.session.add(main_withdrawal_transaction)
        db.session.commit()
        # update customer working balance
        customer.working_bal = round(current_balance, 2)
        db.session.add(customer)
        db.session.commit()
        # -------------------------------
        # Update Till Opening/Closing balance
        self.suspense_account_teller.c_balance += round(self.amount, 2)
        db.session.add(self.suspense_account_teller)
        db.session.commit()
        # -------------------------------

        # 2. charge details between customer and charge account
        # charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = db.session.query(TransactionChargeFee).filter_by(tran_type=TransactionType.DEBIT).first()
        current_balance_after_charge = float(customer.working_bal) - float(get_charge.tran_charge)
        charge_withdrawal_transaction \
            = Transaction(trantype='DR',
                          tranref=Auto.reference_string_generator(),
                          tranmethod='Charge Transfer',
                          tran_date=transaction_reference,
                          cheque_num='None',
                          acc_number=int(self.cr_account),
                          cr_acc_number=int(self.suspense_account_charges.acc_number),
                          amount=float(get_charge.tran_charge),
                          current_balance=round(current_balance_after_charge, 2),
                          remark='Debit Charge',
                          custid=customer.custid)
        db.session.add(charge_withdrawal_transaction)
        db.session.commit()

        # Update Working balance on charge
        customer.working_bal = round(current_balance_after_charge, 2)
        db.session.add(customer)
        db.session.commit()
        # ---------------------------------


class ChargeTransaction:
    """
    Charge Transaction Class handles all the charge logic for Withdrawals, internal transfers,
    external transfers methods:
            charges(transaction_type)
    initialising instance:
            ChargeTransaction(date, dr_account).charges(TransactionType.DEBIT)

    Transaction charges are charges according to the charges tables and each transaction type has
    a charge associated with it

    Todo: change this class to ProcessChargeTransaction
    """

    def __init__(self, date, dr_account):
        self.date = date
        self.dr_account = dr_account
        self.suspense_account_charges = db.session.query(Customer) \
            .filter_by(account_type=AccountTypes.CHARGES.value) \
            .first()
        self.suspense_account_service_fees = db.session.query(Customer) \
            .filter_by(account_type=AccountTypes.SERVICE_FEES.value) \
            .first()

    def charges(self, transaction_type: TransactionType):
        """Service fees go to a different suspense account from the transaction charges."""

        transaction_fee: TransactionFeeChargeTable

        get_charge = db.session.query(TransactionChargeFee) \
            .filter_by(tran_type=transaction_type.value) \
            .first()

        charge_category = [TransactionType.DEBIT, TransactionType.CREDIT, TransactionType.RTGS]

        if transaction_type in charge_category:
            self._commit_change(transaction_type, get_charge.tran_charge)

            # Update charge account working balance
            self.suspense_account_charges.working_bal += get_charge.tran_charge
            db.session.add(self.suspense_account_charges)
            db.session.commit()
        elif transaction_type == TransactionType.SERVICE_FEE:
            self._commit_change(transaction_type, get_charge.tran_charge)

            # Update charge account working balance
            self.suspense_account_service_fees.working_bal += get_charge.tran_charge
            db.session.add(self.suspense_account_service_fees)
            db.session.commit()
        else:
            # SystemOBS().start_logging("transaction charge type not found.")
            "none"

    def _commit_change(self, transaction_type: TransactionType, transaction_charge: float):
        charge = TransactionFeeChargeTable(
            tran_type=transaction_type.value,
            dr_account=self.dr_account,
            cr_account=self.suspense_account_service_fees.acc_number,
            charge=transaction_charge,
            date=self.date)

        db.session.add(charge)
        db.session.commit()


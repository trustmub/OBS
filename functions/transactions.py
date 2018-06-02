import datetime

from cob.log_module import SystemOBS
from functions.Enums import TransactionType, TransactionMethod
from functions.genarators import Auto, Getters
from models.models import Transactions, Customer, Till, ChargeTransactionTable, TransactionCharge

from models.database_connection import session


class Transaction(object):

    def __init__(self, date, amount, cr_account):
        self.date = date
        self.amount = amount
        self.cr_account = cr_account


class CommitTransaction:
    """This class handles the commition of transaction in the database. all parameters have to be supplies inorder
    for the record to be commited to the Transaction table."""

    def __init__(self, trans_type, trans_ref, trans_method, trans_date, cheque_number, dr_account_number,
                 cr_account_number, amount, current_balance, remark, customer_id):
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

    def commit_to_database(self):
        transaction = Transactions(trantype=self.trans_type,
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
        session.add(transaction)
        session.commit()


class AccountTransaction(Transaction):
    """This class handles customer account transaction of diferent types which include account creation, WithDrawals,
    Deposits, Transfers"""

    def __init__(self, date, amount, cr_account):
        Transaction.__init__(self, date, amount, cr_account)
        self.suspense_account_new_account = session.query(Customer).filter_by(account_type='acccreate').first()
        if Getters.getTillDetails() is not None:
            self.suspense_account_teller = session.query(Till).filter_by(
                till_account=Getters.getTillDetails().till_account).first()
        else:
            SystemOBS().start_logging("there is no till details")

        self.suspense_account_charges = session.query(Customer).filter_by(account_type='charges').first()

    """this method does not take any parameter. it create a new account and associates it to the customer ID for the 
    new customer created """

    def create_account(self):
        # suspense_account = session.query(Customer).filter_by(account_type='acccreate').first()
        try:
            customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()
        except ValueError as e:
            print(e)
            SystemOBS().start_logging(e)
            return 0
        # Update transactions Table
        CommitTransaction(TransactionType.CREDIT.value,
                          Auto.reference_string_generator(),
                          TransactionMethod.CASH.value,
                          self.date,
                          'None',
                          self.suspense_account_new_account.acc_number,
                          self.cr_account,
                          self.amount,
                          round(self.amount, 2),
                          'Account Creation',
                          customer.custid) \
            .commit_to_database()

        # update the Account creation Suspense Account
        self.suspense_account_new_account.working_bal -= self.amount
        session.add(self.suspense_account_new_account)
        session.commit()
        SystemOBS().start_logging("Account Created: " + str(customer.acc_number))
        return 1
        # ---------------------------------------------

    """This method takes an additional parameter @transaction_reference for a deposit transaction to be saved in the 
    database. 
    - A deposit affects the Teller Till account, this means theTeller Account is debited and Customer account 
    credited """

    def deposit(self, transaction_reference):
        customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()
        current_balance = float(self.amount) + float(customer.working_bal)

        CommitTransaction(trans_type=TransactionType.CREDIT.value,
                          trans_ref=Auto.reference_string_generator(),
                          trans_method=TransactionMethod.CASH.value,
                          trans_date=self.date,
                          cheque_number='None',
                          dr_account_number=self.suspense_account_teller.till_account,
                          cr_account_number=self.cr_account,
                          amount=self.amount,
                          current_balance=round(current_balance, 2),
                          remark='Deposit_' + transaction_reference,
                          customer_id=customer.custid,
                          ).commit_to_database()

        # Update customers working balance
        customer.working_bal = round(current_balance, 2)
        session.add(customer)
        session.commit()
        # -------------------------------

        # Update Till Opening/Closing   Balance
        self.suspense_account_teller.c_balance -= round(float(self.amount), 2)
        session.add(self.suspense_account_teller)
        session.commit()

    """this methods takes in transaction reference generated at the point of withdrawal and save the record in the 
    Transaction table. in a withdrawal, two transaction record are created, one for the debited account and the other 
    for the credited account. 
    
    - A withdrawal affects the Tellers till balance, this means the Teller account will be 
    credited and customer account debited """

    def withdrawal(self, transaction_reference):
        customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()

        current_balance = float(customer.working_bal) - float(self.amount)
        main_withdrawal_transaction = Transactions(trantype='DR',
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
        session.add(main_withdrawal_transaction)
        session.commit()
        # update customer working balance
        customer.working_bal = round(current_balance, 2)
        session.add(customer)
        session.commit()
        # -------------------------------
        # Update Till Opening/Closing balance
        self.suspense_account_teller.c_balance += round(self.amount, 2)
        session.add(self.suspense_account_teller)
        session.commit()
        # -------------------------------

        # 2. charge details between customer and charge account
        # charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = session.query(TransactionCharge).filter_by(tran_type='DR').first()
        current_balance_after_charge = float(customer.working_bal) - float(get_charge.tran_charge)
        charge_withdrawal_transaction = Transactions(trantype='DR',
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
        session.add(charge_withdrawal_transaction)
        session.commit()

        # Update Working balance on charge
        customer.working_bal = round(current_balance_after_charge, 2)
        session.add(customer)
        session.commit()
        # ---------------------------------


class ChargeTransaction:
    """ Charge Transaction Class handles all the charge logic for Withdrawals, internal transfers, external transfers
    methods:
            charges(transaction_type)
    initialising instance:
            ChargeTransaction(date, dr_account).charges(TransactionType.DEBIT)

    Transaction charges are charges according to the charges tables and each transactio type has a charge associated
    with it """

    def __init__(self, date, dr_account):
        self.date = date
        self.dr_account = dr_account
        self.suspense_account_charges = session.query(Customer).filter_by(account_type='charges').first()
        self.suspense_account_service_fees = session.query(Customer).filter_by(account_type='servfee').first()

    def charges(self, transaction_type):
        """Service fees go to a different suspense account from the transaction charges."""

        get_charge = session.query(TransactionCharge).filter_by(tran_type=transaction_type.value).first()

        charge_category = [TransactionType.DEBIT, TransactionType.CREDIT, TransactionType.RTGS]

        if transaction_type in charge_category:
            charge_transaction = ChargeTransactionTable(
                tran_type=transaction_type.value,
                dr_account=self.dr_account,
                cr_account=self.suspense_account_charges.acc_number,
                charge=get_charge.tran_charge,
                date=self.date
            )
            session.add(charge_transaction)
            session.commit()
            # Update charge account working balance
            self.suspense_account_charges.working_bal += get_charge.tran_charge
            session.add(self.suspense_account_charges)
            session.commit()
        elif transaction_type == TransactionType.SERVICE_FEE:
            new = ChargeTransactionTable(
                tran_type=transaction_type.value,
                dr_account=self.dr_account,
                cr_account=self.suspense_account_service_fees.acc_number,
                charge=get_charge.tran_charge,
                date=self.date)
            session.add(new)
            session.commit()
            # Update charge account working balance
            self.suspense_account_service_fees.working_bal += get_charge.tran_charge
            session.add(self.suspense_account_service_fees)
            session.commit()
        else:
            SystemOBS().logger.error().start_logging("transaction charge type not found.")
            pass

from sqlalchemy.orm import sessionmaker
import datetime

from functions.Enums import TransactionType, TransactionMethod
from functions.genarators import Auto, Getters
from models import *

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
                                   custid=self.customer_id,
                                   create_date=datetime.datetime.now())
        session.add(transaction)
        session.commit()


class AccountTransaction(Transaction):
    """This class handles customer account transaction of diferent types which include account creation, WithDrawals,
    Deposits, Transfers"""

    def __init__(self, date, amount, cr_account):
        Transaction.__init__(self, date, amount, cr_account)

    """this method does not take any parameter. it create a new account and associates it to the customer ID for the 
    new customer created """

    def create_account(self):
        suspense_account = session.query(Customer).filter_by(account_type='acccreate').first()
        customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()
        # Update transactions Table
        CommitTransaction(TransactionType.CREDIT.value,
                          Auto.referenceStringGen(),
                          TransactionMethod.CASH.value,
                          self.date,
                          'None',
                          suspense_account.acc_number,
                          self.cr_account,
                          self.amount,
                          round(self.amount, 2),
                          'Account Creation',
                          customer.custid) \
            .commit_to_database()

        # update the Account creation Suspense Account
        suspense_account.working_bal -= self.amount
        session.add(suspense_account)
        session.commit()
        # ---------------------------------------------

    """This method takes an additional parameter @transaction_reference for a deposit transaction to be saved in the 
    database. 
    - A deposit affects the Teller Till account, this means theTeller Account is debited and Customer account 
    credited """

    def deposit(self, transaction_reference):
        customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()
        current_balance = float(self.amount) + float(customer.working_bal)

        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        CommitTransaction(trans_type=TransactionType.CREDIT.value,
                          trans_ref=Auto.referenceStringGen(),
                          trans_method=TransactionMethod.CASH.value,
                          trans_date=self.date,
                          cheque_number='None',
                          dr_account_number=(till_detail.till_account),
                          cr_account_number=self.cr_account,
                          amount=self.amount,
                          current_balance=round(current_balance, 2),
                          remark='Deposit_' + transaction_reference,
                          customer_id=customer.custid,
                          ).commit_to_database()

        # Update customer working balance
        customer.working_bal = round(current_balance, 2)
        session.add(customer)
        session.commit()
        # -------------------------------

        # Update Till Opening/Closing   Balance
        till_detail.c_balance -= round(float(self.amount), 2)
        session.add(till_detail)
        session.commit()

    """this methods takes in transaction reference generated at the point of withdrawal and save the record in the 
    Transaction table. in a withdrawal, two transaction record are created, one for the debited account and the other 
    for the credited account. 
    
    - A withdrawal affects the Tellers till balance, this means the Teller account will be 
    credited and customer account debited """

    def withdrawal(self, transaction_reference):
        customer = session.query(Customer).filter_by(acc_number=self.cr_account).one()
        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        cb = float(customer.working_bal) - float(self.amount)
        trans = Transactions(trantype='DR',
                             tranref=transaction_reference,
                             tranmethod='Cash',
                             tran_date=self.date,
                             cheque_num='None',
                             acc_number=int(self.cr_account),
                             cr_acc_number=int(till_detail.till_account),
                             amount=self.amount,
                             current_balance=round(cb, 2),
                             remark='Withdrawal ' + transaction_reference,
                             custid=customer.custid,
                             create_date=datetime.datetime.now())
        session.add(trans)
        session.commit()
        # update customer working balance
        customer.working_bal = round(cb, 2)
        session.add(customer)
        session.commit()
        # -------------------------------
        # Update Till Opening/Closing balance
        till_detail.c_balance += round(self.amount, 2)
        session.add(till_detail)
        session.commit()
        # -------------------------------

        # 2. charge details between customer and charge account
        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = session.query(TransactionCharge).filter_by(tran_type='DR').first()
        cb2 = float(customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transactions(trantype='DR',
                              tranref=Auto.referenceStringGen(),
                              tranmethod='Charge Transfer',
                              tran_date=transaction_reference,
                              cheque_num='None',
                              acc_number=int(self.cr_account),
                              cr_acc_number=int(charge_account.acc_number),
                              amount=float(get_charge.tran_charge),
                              current_balance=round(cb2, 2),
                              remark='Debit Charge',
                              custid=customer.custid,
                              create_date=datetime.datetime.now())
        session.add(trans2)
        session.commit()

        # Update Working balance on charge
        customer.working_bal = round(cb2, 2)
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

    def charges(self, transaction_type):
        get_charge = session.query(TransactionCharge).filter_by(tran_type=transaction_type.value).first()

        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        servfee = session.query(Customer).filter_by(account_type='servfee').first()

        charge_category = [TransactionType.DEBIT, TransactionType.CREDIT, TransactionType.RTGS]

        if transaction_type in charge_category:
            charge_transaction = ChargeTransactionTable(
                tran_type=transaction_type.value,
                dr_account=self.dr_account,
                cr_account=charge_account.acc_number,
                charge=get_charge.tran_charge,
                date=self.date,
                create_date=datetime.datetime.now()
            )
            session.add(charge_transaction)
            session.commit()
            # Update charge account working balance
            charge_account.working_bal += get_charge.tran_charge
            session.add(charge_account)
            session.commit()

        elif transaction_type == TransactionType.SERVICE_FEE:
            new = ChargeTransactionTable(
                tran_type=transaction_type.value,
                dr_account=self.dr_account,
                cr_account=servfee.acc_number,
                charge=get_charge.tran_charge,
                date=self.date,
                create_date=datetime.datetime.now()
            )
            session.add(new)
            session.commit()
            # Update charge account working balance
            servfee.working_bal += get_charge.tran_charge
            session.add(servfee)
            session.commit()
        else:
            pass

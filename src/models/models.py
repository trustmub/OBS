"""
This files handled all the models
"""
import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.models import create_engine
from sqlalchemy.dialects import postgresql

BASE = declarative_base()


class User(BASE):
    """
    This table contains all the systems users from the teller, backend operations and system users.
    """
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    job_title = Column(String(100))
    image_string = Column(String(100))
    department = Column(String(50))
    branch_code = Column(String(15))
    access_level = Column(Integer)
    till_o_balance = Column(Float(2))
    till_c_balance = Column(Float(2))
    create_date = Column(String(30))
    email = Column(String(60))
    password = Column(String(100))
    lock = Column(Integer)

    def __init__(self, full_name,
                 job_title,
                 image_string,
                 department,
                 branch_code,
                 access_level,
                 till_o_balance,
                 till_c_balance,
                 email,
                 password,
                 lock):
        self.full_name = full_name
        self.job_title = job_title
        self.image_string = image_string
        self.department = department
        self.branch_code = branch_code
        self.access_level = access_level
        self.till_o_balance = till_o_balance
        self.till_c_balance = till_c_balance
        self.create_date = datetime.datetime.now()
        self.email = email
        self.password = password
        self.lock = lock

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return "{} the {}".format(self.full_name, self.job_title)

    def add_user(self):
        return


class ApiUser(BASE):
    """
    This table is for mobile users access through the API
    """
    __tablename__ = 'api_user'
    user_id = Column(Integer, primary_key=True)
    account_number = Column(Integer)
    device = Column(String(50))
    pin = Column(String(100))
    user_number = Column(Integer)

    def __init__(self, account_number, device, pin, user_number):
        self.account_number = account_number
        self.device = device
        self.pin = pin
        self.user_number = user_number

    @property
    def serialize(self):
        return {
            'account': self.account_number,
            'user_number': self.user_number,
            'device': str(self.device)
        }


class BankingServices(BASE):
    __tablename__ = 'banking_services'
    id = Column(Integer, primary_key=True)
    service_name = Column(String(50))
    service_description = Column(String(200))
    created_date = Column(String(30))

    def __init__(self, service_name, service_description):
        self.service_name = service_name
        self.service_description = service_description
        self.created_date = datetime.datetime.now()


class CustomerBankingService(BASE):
    __tablename__ = "registered_services"
    id = Column(Integer, primary_key=True)
    api_user_id = Column(Integer, ForeignKey('api_user.user_id'))
    api_user = relationship(ApiUser)
    service_id = Column(Integer, ForeignKey('banking_services.id'))
    service = relationship(BankingServices)
    status = Column(String(10))
    created_date = Column(String(30))

    def __init__(self, api_user_id, service_id, status):
        self.api_user_id = api_user_id
        self.service_id = service_id
        self.status = status
        self.created_date = datetime.datetime.now()

    @property
    def serialize(self):
        return {
            "name": self.service.service_name,
            "status": self.status
        }


class Card(BASE):
    __tablename__ = "card"
    id = Column(Integer, primary_key=True)
    card_number = Column(String(15))
    account_number = Column(Integer)
    card_type = Column(String(100))
    created_date = Column(String(30))

    def __init__(self, card_number, account_number, card_type, created_date):
        self.card_number = card_number
        self.account_number = account_number
        self.card_type = card_type
        self.created_date = datetime.datetime.now()

    @property
    def serialize(self):
        return {
            "id": self.id,
            "card": self.card_number,
            "account": self.account_number,
            "type": self.card_type
        }


class Customer(BASE):
    """
    THis table contains all the customer details.
    """
    __tablename__ = 'customer'
    custid = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    dob = Column(String(15))
    address = Column(String(256))
    country = Column(String(100))
    email = Column(String(100))
    gender = Column(String(30))
    contact_number = Column(String(20))
    working_bal = Column(Float(2))
    acc_number = Column(Integer)
    account_type = Column(String(10))
    create_date = Column(String(30))
    # services = Column(postgresql.ARRAY(Integer, dimensions=1))
    # signature_img = Column(String(100))

    card_id = Column(Integer, ForeignKey("card.id"))
    card = relationship(Card)

    inputter_id = Column(Integer, ForeignKey('user.uid'))
    inputter = relationship(User)

    def __init__(self, first_name,
                 last_name,
                 dob,
                 address,
                 country,
                 email,
                 gender,
                 contact_number,
                 working_bal,
                 acc_number,
                 account_type,
                 create_date,
                 inputter_id):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.address = address
        self.country = country
        self.email = email
        self.gender = gender
        self.contact_number = contact_number
        self.working_bal = working_bal
        self.acc_number = acc_number
        self.account_type = account_type
        self.create_date = create_date
        self.inputter_id = inputter_id

    @property
    def full_name(self):
        """
        full name as a property
        :return: first_name and last_name
        """
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def serialize(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'balance': self.working_bal,
            'account_type': self.account_type,
            'account_number': self.acc_number
        }


class Account(BASE):
    """
    This table contains the type of accounts the systems handles for example, Savings current of
    Corporate Account
    """
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    acc_type = Column(String(10))
    minbalance = Column(Integer)

    def __init__(self, acc_type, minbalance):
        self.acc_type = acc_type
        self.minbalance = minbalance

    def __str__(self):
        return "account type: {}".format(self.acc_type)


class Transactions(BASE):
    """
    This table contains all the client transaction that are done in the system. these include
    Withdrawal, Deposits, transfers that affect the client account.
    """
    __tablename__ = 'transactions'
    tranid = Column(Integer, primary_key=True)
    trantype = Column(String(10))
    tranref = Column(String(15))
    tranmethod = Column(String(50))
    tran_date = Column(String(30))
    cheque_num = Column(String(30))
    acc_number = Column(Integer)
    cr_acc_number = Column(Integer)
    amount = Column(Float(2))
    current_balance = Column(Float(2))
    remark = Column(String(200))

    custid = Column(Integer, ForeignKey('customer.custid'))
    customer = relationship(Customer)

    create_date = Column(String(30))

    def __init__(self, trantype,
                 tranref,
                 tranmethod,
                 tran_date,
                 cheque_num,
                 acc_number,
                 cr_acc_number,
                 amount,
                 current_balance,
                 remark,
                 custid):
        self.trantype = trantype
        self.tranref = tranref
        self.tranmethod = tranmethod
        self.tran_date = tran_date
        self.cheque_num = cheque_num
        self.acc_number = acc_number
        self.cr_acc_number = cr_acc_number
        self.amount = amount
        self.current_balance = current_balance
        self.remark = remark
        self.custid = custid
        self.create_date = datetime.datetime.now()

    def __str__(self):
        return self.tranref


class TransactionCharge(BASE):
    """
    This table keeps the charge fees for each respective Transaction type. additional transaction
    typex can be added in the transaction type table
    TODO Transaction type table
    """
    __tablename__ = 'transactioncharge'
    id = Column(Integer, primary_key=True)
    tran_type = Column(String(10))
    tran_charge = Column(Float(2))
    create_date = Column(String(30))

    def __init__(self, tran_type, tran_charge):
        self.tran_type = tran_type
        self.tran_charge = tran_charge
        self.create_date = datetime.datetime.now()

    def __str__(self):
        return "{} charged {}".format(self.tran_type, self.tran_charge)


class ChargeTransactionTable(BASE):
    """
    This table contains all the transactions for charges that the clients have been charged on
    their operations including service fees. Windrawal and frasnfer charges are also captured in
    here with apropriate reference to show the type of charge.
    """
    __tablename__ = 'chargetransaction'
    id = Column(Integer, primary_key=True)
    tran_type = Column(String(10))
    dr_account = Column(Integer)
    cr_account = Column(Integer)
    charge = Column(Float(2))
    date = Column(String(30))
    create_date = Column(String(30))

    def __init__(self, tran_type, dr_account, cr_account, charge, date):
        self.tran_type = tran_type
        self.dr_account = dr_account
        self.cr_account = cr_account
        self.charge = charge
        self.date = date
        self.create_date = datetime.datetime.now()

    def __str__(self):
        return "DR Account {} Credit Account {}".format(self.cr_account, self.dr_account)


class Till(BASE):
    """
    This table keeps the teller accounts and each teller account is linked to a user_view ID which
    helps to identify the user_view who is linked to the teller account for tracking transactions
    flow.
    """
    __tablename__ = 'till'
    id = Column(Integer, primary_key=True)
    branch_code = Column(String(10))
    o_balance = Column(Float(2))
    c_balance = Column(Float(2))
    till_account = Column(String(15))
    currency = Column(String())
    remark = Column(String(100))
    date = Column(String(30))
    create_date = Column(String(30))

    user_id = Column(Integer, ForeignKey('user.uid'), nullable=True)
    user = relationship(User)

    def __init__(self, branch_code,
                 o_balance,
                 c_balance,
                 till_account,
                 currency,
                 remark,
                 date,
                 create_date,
                 user_id):
        self.branch_code = branch_code
        self.o_balance = o_balance
        self.c_balance = c_balance
        self.till_account = till_account
        self.currency = currency
        self.remark = remark
        self.date = date
        self.create_date = create_date
        self.user_id = user_id

    def __str__(self):
        return self.till_account


class TellerTransactions(BASE):
    """
    This table contains all the transactions a teller does. Each transaction a teller does i
    linked to their teller ID and the Till Account ID. The transaction is also linked to the client
    Account ID enabling a complete trail of the transaction flow.
    """
    __tablename__ = 'tellertransactions'
    id = Column(Integer, primary_key=True)
    tran_type = Column(String(10))
    tranref = Column(String(15))
    amount = Column(Float(2))
    date = Column(String(30))
    remark = Column(String(100))
    create_date = Column(String(30))

    teller_id = Column(Integer, ForeignKey('till.id'))
    teller = relationship(Till)

    customer_id = Column(Integer, ForeignKey('customer.custid'))
    customer = relationship(Customer)

    user_id = Column(Integer, ForeignKey('user.uid'))
    user = relationship(User)

    def __init__(self, tran_type,
                 tranref,
                 amount,
                 date,
                 remark,
                 create_date,
                 teller_id,
                 customer_id,
                 user_id):
        self.tran_type = tran_type
        self.tranref = tranref
        self.amount = amount
        self.date = date
        self.remark = remark
        self.create_date = create_date
        self.teller_id = teller_id
        self.customer_id = customer_id
        self.user_id = user_id


class Currency(BASE):
    """
    This table contains all the currencies the system will be working using. the currencies will be
    added as the operations needs may be.
    """
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    currency_code = Column(String(5))
    description = Column(String(100))
    create_date = Column(String(30))

    def __init__(self, currency_code, description, create_date):
        self.currency_code = currency_code
        self.description = description
        self.create_date = create_date


class Branch(BASE):
    """
    This is the table for branches and their codes. Each account belongs to a particular branch the
    default branch is the head office (01) which will be created during the system setup process.
    """
    __tablename__ = 'branch'
    id = Column(Integer, primary_key=True)
    code = Column(String(5))
    description = Column(String(100))
    create_date = Column(String(30))

    def __init__(self, code, description):
        self.code = code
        self.description = description
        self.create_date = datetime.datetime.now()


class Interest(BASE):
    """
    This is the table where interest earnings are captured. the end of day process calculates the
    interest daily for each account and saves the values into this table for the End O Month
    preocess to credit the interest earned into the respective accounts as a total figure.
    """
    __tablename__ = 'interest'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    account = Column(Integer)
    eod_bal = Column(Float(2))
    interest_earned = Column(Float(2))
    create_date = Column(String(30))

    def __init__(self, date, account, eod_bal, interest_earned):
        self.date = date
        self.account = account
        self.eod_bal = eod_bal
        self.interest_earned = interest_earned
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return "Interest({}, {}, {}, {})".format(self.date,
                                                 self.account,
                                                 self.eod_bal,
                                                 self.interest_earned)

    def __str__(self):
        return self.account


class Banks(BASE):
    """
    This table contains a list of other banks which contains swift codes. This is used for external
    transfers.
    """
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    swift_code = Column(String(50))
    create_date = Column(String(30))

    def __init__(self, name, swift_code):
        self.name = name
        self.swift_code = swift_code
        self.create_date = datetime.datetime.now()

    def __repr__(self):
        return "Banks({}, {})".format(self.name, self.swift_code)

    def __str__(self):
        return self.name


# Complete Of Business tables

class CobDates(BASE):
    """
    This table keeps a list of all the processes that have been run and marks the process with the
    system date so that if the system crashes and the EOD is reinitiated, the processes that have
    executed will not be executed again.
    """
    __tablename__ = 'cobdates'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    process = Column(String(50))
    status = Column(Integer)
    create_date = Column(String(30))

    def __init__(self, date, process, status, create_date):
        self.date = date
        self.process = process
        self.status = status
        self.create_date = create_date

    def __repr__(self):
        return "CabDates({}, {}, {})".format(self.date,
                                             self.process,
                                             self.status)

    def __str__(self):
        return self.process


class SysDate(BASE):
    """
    This table keeps the current system date since the last End Of Day (EOD) process. When the end
    of day completes the date is changes to the next trading date.
    """
    __tablename__ = 'sysdate'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    create_date = Column(String(30))

    def __init__(self, date, create_date):
        self.date = date
        self.create_date = create_date

    def __repr__(self):
        return "SysDate({}, {})".format(self.date,
                                        self.create_date)

    def __str__(self):
        return self.date


# insert this at the end of the classes #######


ENGINE = create_engine('sqlite:///bank_database.db')
BASE.metadata.create_all(ENGINE)

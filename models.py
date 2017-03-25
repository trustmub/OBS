import os
import sys

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, extract

Base = declarative_base()


class User(Base):
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

    def __init__(self, full_name, job_title, image_string, department, branch_code, access_level, till_o_balance,
                 till_c_balance,
                 create_date, email, password, lock):
        self.full_name = full_name
        self.job_title = job_title
        self.image_string = image_string
        self.department = department
        self.branch_code = branch_code
        self.access_level = access_level
        self.till_o_balance = till_o_balance
        self.till_c_balance = till_c_balance
        self.create_date = create_date
        self.email = email
        self.password = password
        self.lock = lock


class Customer(Base):
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
    # signature_img = Column(String(100))

    inputter_id = Column(Integer, ForeignKey('user.uid'))
    inputter = relationship(User)

    def __init__(self, first_name, last_name, dob, address, country, email, gender, contact_number, working_bal,
                 acc_number, account_type, create_date, inputter_id):
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


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    acc_type = Column(String(10))
    minbalance = Column(Integer)

    def __init__(self, acc_type, minbalance):
        self.acc_type = acc_type
        self.minbalance = minbalance


class Transactions(Base):
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

    def __init__(self, trantype, tranref, tranmethod, tran_date, cheque_num, acc_number, cr_acc_number, amount,
                 current_balance,
                 remark, custid,
                 create_date):
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
        self.create_date = create_date


class TransactionCharge(Base):
    __tablename__ = 'transactioncharge'
    id = Column(Integer, primary_key=True)
    tran_type = Column(String(10))
    tran_charge = Column(Float(2))
    create_date = Column(String(30))

    def __init__(self, tran_type, tran_charge, create_date):
        self.tran_type = tran_type
        self.tran_charge = tran_charge
        self.create_date = create_date


class ChargeTransactionTable(Base):
    __tablename__ = 'chargetransaction'
    id = Column(Integer, primary_key=True)
    tran_type = Column(String(10))
    dr_account = Column(Integer)
    cr_account = Column(Integer)
    charge = Column(Float(2))
    date = Column(String(30))
    create_date = Column(String(30))

    def __init__(self, tran_type, dr_account, cr_account, charge, date, create_date):
        self.tran_type = tran_type
        self.dr_account = dr_account
        self.cr_account = cr_account
        self.charge = charge
        self.date = date
        self.create_date = create_date


class Till(Base):
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

    def __init__(self, branch_code, o_balance, c_balance, till_account, currency, remark, date, create_date, user_id):
        self.branch_code = branch_code
        self.o_balance = o_balance
        self.c_balance = c_balance
        self.till_account = till_account
        self.currency = currency
        self.remark = remark
        self.date = date
        self.create_date = create_date
        self.user_id = user_id


class TellerTransactions(Base):
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

    def __init__(self, tran_type, tranref, amount, date, remark, create_date, teller_id, customer_id, user_id):
        self.tran_type = tran_type
        self.tranref = tranref
        self.amount = amount
        self.date = date
        self.remark = remark
        self.create_date = create_date
        self.teller_id = teller_id
        self.customer_id = customer_id
        self.user_id = user_id


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    currency_code = Column(String(5))
    description = Column(String(100))
    create_date = Column(String(30))

    def __init__(self, currency_code, description, create_date):
        self.currency_code = currency_code
        self.description = description
        self.create_date = create_date


class Branch(Base):
    __tablename__ = 'branch'
    id = Column(Integer, primary_key=True)
    code = Column(String(5))
    description = Column(String(100))
    create_date = Column(String(30))

    def __init__(self, code, description, create_date):
        self.code = code
        self.description = description
        self.create_date = create_date


class Interest(Base):
    __tablename__ = 'interest'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    account = Column(Integer)
    eod_bal = Column(Float(2))
    interest_earned = Column(Float(2))
    create_date = Column(String(30))

    def __init__(self, date, account, eod_bal, interest_earned, create_date):
        self.date = date
        self.account = account
        self.eod_bal = eod_bal
        self.interest_earned = interest_earned
        self.create_date = create_date


class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    swift_code = Column(String(50))
    create_date = Column(String(30))

    def __init__(self, name, swift_code, create_date):
        self.name = name
        self.swift_code = swift_code
        self.create_date = create_date


# Complete Of Business tables

class CobDates(Base):
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


class SysDate(Base):
    __tablename__ = 'sysdate'
    id = Column(Integer, primary_key=True)
    date = Column(String(30))
    create_date = Column(String(30))

    def __init__(self, date, create_date):
        self.date = date
        self.create_date = create_date


# insert this at the end of the classes #######


engine = create_engine('sqlite:///bnk.db')
Base.metadata.create_all(engine)
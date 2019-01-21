import time
import datetime
from src.models import session
from src.models.models import SysDate, Till, TransactionCharge, Account, Branch, Currency, Customer, BankingServices
from src.functions.genarators import Auto

# print("Creating System Date")
# sys_date = SysDate(date=time.strftime('%Y-%m-%d'), create_date=datetime.datetime.now())
# session.add(sys_date)
# session.commit()

# print("Done creating system Date")
"""
rtgs = Customer(first_name='sys_user', last_name='sys_user', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto().account_number_generator(), account_type='rtgs', create_date=datetime.datetime.now(),
                inputter_id=1)
print("RTGS Account Created")
new = Customer(first_name='sys_user1', last_name='sys_user1', dob=time.strftime('%Y-%m-%d'), address='address',
               country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
               acc_number=Auto().account_number_generator(), account_type='charges',
               create_date=datetime.datetime.now(),
               inputter_id=1)

print("Charges Account Created : " + new.first_name, new.last_name, new.acc_number)
new1 = Customer(first_name='sys_user2', last_name='sys_user2', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto().account_number_generator(), account_type='suspense',
                create_date=datetime.datetime.now(),
                inputter_id=1)
print("Teller Suspense Account Created : " + new1.first_name, new1.last_name, new1.acc_number)
new2 = Customer(first_name='PL52232', last_name='PL52232', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto().account_number_generator(), account_type='servfee',
                create_date=datetime.datetime.now(),
                inputter_id=1)
print("Service Fee Account Created" + new2.first_name, new2.last_name, new2.acc_number)
new3 = Customer(first_name='sys_user4', last_name='sys_user4', dob=time.strftime('%Y-%m-%d'), address='Address',
                country='Zimbabwe', email='System', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto().account_number_generator(), account_type='acccreate',
                create_date=datetime.datetime.now(),
                inputter_id=1)
print("Account Creation Suspense Account Created" + new2.first_name, new2.last_name, new2.acc_number)
new4 = Customer(first_name='sys_user4', last_name='sys_user4', dob=time.strftime('%Y-%m-%d'), address='Address',
                country='Zimbabwe', email='System', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto().account_number_generator(), account_type='interest',
                create_date=datetime.datetime.now(),
                inputter_id=1)
print("Interests Suspense Account Created Created" + new3.first_name, new3.last_name, new3.acc_number)
# all deposits to this account will be moved at monthend to the respective branch suspense accounts
session.add(new)
session.add(rtgs)
session.add(new1)
session.add(new2)
session.add(new3)
session.add(new4)
session.commit()
"""


def create_system_tellers():
    for _ in range(0, 6):
        new_teller = Till(branch_code='', o_balance=0, c_balance=0,
                          till_account=Auto().system_account_number_generator(),
                          currency="USD", remark='', date='', create_date=datetime.datetime.now(), user_id='')
        session.add(new_teller)
        session.commit()


# teller1 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto().system_account_number_generator(),
#                currency='USD',
#                remark='', date='', create_date=datetime.datetime.now(), user_id='')
# print("Teller Created")
# teller2 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto().system_account_number_generator(),
#                currency='USD',
#                remark='', date='', create_date=datetime.datetime.now(), user_id='')
# print("Teller Created")
# teller3 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto().system_account_number_generator(),
#                currency='USD',
#                remark='', date='', create_date=datetime.datetime.now(), user_id='')
# print("Teller Created")
# teller4 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto().system_account_number_generator(),
#                currency='USD',
#                remark='', date='', create_date=datetime.datetime.now(), user_id='')
# print("Teller Created")
# session.add(teller1)
# session.add(teller2)
# session.add(teller3)
# session.add(teller4)
# session.commit()
#

def create_system_currencies():
    currencies = [{"currency_code": "USD", "description": "United States Dollar"},
                  {"currency_code": "ZAR", "description": "South African Rand"},
                  {"currency_code": "GBP", "description": "Great Britain Pound"}]

    for currency in currencies:
        code = currency.get("currency_code")
        description = currency.get("description")
        if code not in [c.currency_code for c in session.query(Currency).all()]:
            new_currency = Currency(currency_code=code, description=description, create_date=datetime.datetime.now())
            session.add(new_currency)
            session.commit()
        else:
            continue


# currency1 = Currency(currency_code='USD', description='United States Dollar', create_date=datetime.datetime.now())
# print("USD Currency Created")
# currency2 = Currency(currency_code='ZAR', description='South African Rand', create_date=datetime.datetime.now())
# print("ZAR Currency Created")
# currency3 = Currency(currency_code='GBP', description='Great Britain Pound', create_date=datetime.datetime.now())
# print("GBP Currency Created")
# session.add(currency1)
# session.add(currency2)
# session.add(currency3)
# session.commit()


def create_system_branches():
    branches = [{"code": "01", "description": "Head Office"},
                {"code": "02", "description": "Treasury"},
                {"code": "03", "description": "Reconciliation"}]
    for branch in branches:
        branch_code = branch.get("code")
        description = branch.get("description")
        if branch_code not in [b.code for b in session.query(Branch).all()]:
            new_branch = Branch(code=branch_code, description=description)
            session.add(new_branch)
            session.commit()
        else:
            continue


# branch1 = Branch(code='33', description='Head Office')
# branch2 = Branch(code='40', description='Durban Branch')
# branch3 = Branch(code='21', description='Pretoria Branch')
# print("Initial branch Created")
# session.add(branch1)
# session.add(branch2)
# session.add(branch3)
# session.commit()


def create_transaction_charge_type():
    charge_types = [{"tran_type": "CR", "tran_charge": 0},
                    {"tran_type": "DR", "tran_charge": 1.50},
                    {"tran_type": "TR", "tran_charge": 1.0},
                    {"tran_type": "RTGS", "tran_charge": 5.0},
                    {"tran_type": "SF", "tran_charge": 3.0}]

    for charge in charge_types:
        trans_type = charge.get("tran_type")
        trans_charge = charge.get("tran_charge")
        if trans_type not in [chg.tran_type for chg in session.query(TransactionCharge).all()]:
            new_charge = TransactionCharge(tran_type=trans_type, tran_charge=trans_charge)
            session.add(new_charge)
            session.commit()
            print("Charge Type created")
        else:
            continue


# charges1 = TransactionCharge(tran_type='CR', tran_charge=0)
# charges2 = TransactionCharge(tran_type='DR', tran_charge=1.50)
# charges3 = TransactionCharge(tran_type='TR', tran_charge=1.0)
# charges4 = TransactionCharge(tran_type='RTGS', tran_charge=5.0)
# charges5 = TransactionCharge(tran_type='SF', tran_charge=3.0)
# print("Basic Charges Created")
# session.add(charges1)
# session.add(charges2)
# session.add(charges3)
# session.add(charges4)
# session.add(charges5)
# session.commit()


def create_account_type():
    account_types = [{"acc_type": "Savings", "minbalance": 0},
                     {"acc_type": "Current", "minbalance": 5},
                     {"acc_type": "Corporate", "minbalance": 100}]
    for type in account_types:
        type_name = type.get("acc_type")
        min_balance = type.get("minbalance")
        if type_name not in [t.acc_type for t in session.query(Account).filter_by(acc_type=type_name).all()]:
            new_type = Account(acc_type=type_name, minbalance=min_balance)
            print("Account types created")
            session.add(new_type)
            session.commit()
        else:
            continue


# acc1 = Account(acc_type='Savings', minbalance=0)
# acc2 = Account(acc_type='Current', minbalance=5)
# acc3 = Account(acc_type='Corporate', minbalance=100)
# print("Account types created")
# session.add(acc1)
# session.add(acc2)
# session.add(acc3)
# session.commit()


def create_banking_services():
    service_dictionary = [{"service_name": "Pay", "service_description": "for payments"},
                          {"service_name": "Transfer", "service_description": "Transfer funds to local banks"},
                          {"service_name": "CashSend", "service_description": "E-wallet services"},
                          {"service_name": "Bill Payments", "service_description": "Bill Payments"}]
    for service in service_dictionary:

        service_n = service.get("service_name")
        service_d = service.get("service_description")

        if service_n not in [s.service_name for s in
                             session.query(BankingServices).filter_by(service_name=service_n).all()]:
            service_record = BankingServices(service_name=service_n, service_description=service_d)
            print("Banking service: {} create".format(service_n))
            session.add(service_record)
            session.commit()
        else:
            continue


def create_application_defaults():
    create_system_currencies()
    create_system_branches()
    create_transaction_charge_type()
    create_banking_services()
    create_account_type()


if __name__ == '__main__':
    create_application_defaults()

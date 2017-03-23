from views.customer import *

print("Creating System Date")
sys_date = SysDate(date=time.strftime('%Y-%m-%d'), create_date=datetime.datetime.now())
session.add(sys_date)
session.commit()

print("Done creating system Date")

rtgs = Customer(first_name='sys_user', last_name='sys_user', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto.accountNumGen(), account_type='rtgs', create_date=datetime.datetime.now(),
                inputter_id=1)
print("RTGS Account Created")
new = Customer(first_name='sys_user1', last_name='sys_user1', dob=time.strftime('%Y-%m-%d'), address='address',
               country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
               acc_number=Auto.accountNumGen(), account_type='charges', create_date=datetime.datetime.now(),
               inputter_id=1)

print("Charges Account Created : " + new.first_name, new.last_name, new.acc_number)
new1 = Customer(first_name='sys_user2', last_name='sys_user2', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto.accountNumGen(), account_type='suspense', create_date=datetime.datetime.now(),
                inputter_id=1)
print("Teller Suspense Account Created : " + new1.first_name, new1.last_name, new1.acc_number)
new2 = Customer(first_name='PL52232', last_name='PL52232', dob=time.strftime('%Y-%m-%d'), address='address',
                country='Zimbabwe', email='system', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto.accountNumGen(), account_type='servfee', create_date=datetime.datetime.now(),
                inputter_id=1)
print("Service Fee Account Created" + new2.first_name, new2.last_name, new2.acc_number)
new3 = Customer(first_name='sys_user4', last_name='sys_user4', dob=time.strftime('%Y-%m-%d'), address='Address',
                country='Zimbabwe', email='System', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto.accountNumGen(), account_type='acccreate', create_date=datetime.datetime.now(),
                inputter_id=1)
print("Account Creation Suspense Account Created" + new2.first_name, new2.last_name, new2.acc_number)
new4 = Customer(first_name='sys_user4', last_name='sys_user4', dob=time.strftime('%Y-%m-%d'), address='Address',
                country='Zimbabwe', email='System', gender='system', contact_number='09100000', working_bal=0,
                acc_number=Auto.accountNumGen(), account_type='interest', create_date=datetime.datetime.now(),
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

teller1 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto.systemAccNumberGen(), currency='USD',
               remark='', date='', create_date=datetime.datetime.now(), user_id='')
print("Teller Created")
teller2 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto.systemAccNumberGen(), currency='USD',
               remark='', date='', create_date=datetime.datetime.now(), user_id='')
print("Teller Created")
teller3 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto.systemAccNumberGen(), currency='USD',
               remark='', date='', create_date=datetime.datetime.now(), user_id='')
print("Teller Created")
teller4 = Till(branch_code='', o_balance=0, c_balance=0, till_account=Auto.systemAccNumberGen(), currency='USD',
               remark='', date='', create_date=datetime.datetime.now(), user_id='')
print("Teller Created")
session.add(teller1)
session.add(teller2)
session.add(teller3)
session.add(teller4)
session.commit()

currency1 = Currency(currency_code='USD', description='United States Dollar', create_date=datetime.datetime.now())
print("USD Currency Created")
currency2 = Currency(currency_code='ZAR', description='South African Rand', create_date=datetime.datetime.now())
print("ZAR Currency Created")
currency3 = Currency(currency_code='GBP', description='Great Britain Pound', create_date=datetime.datetime.now())
print("GBP Currency Created")
session.add(currency1)
session.add(currency2)
session.add(currency3)
session.commit()

branch1 = Branch(code='33', description='Head Office', create_date=datetime.datetime.now())
branch2 = Branch(code='40', description='Bulawayo Branch', create_date=datetime.datetime.now())
branch3 = Branch(code='21', description='Masvingo Branch', create_date=datetime.datetime.now())
print("Initial branch Created")
session.add(branch1)
session.add(branch2)
session.add(branch3)
session.commit()

charges1 = TransactionCharge(tran_type='CR', tran_charge=0, create_date=datetime.datetime.now())
charges2 = TransactionCharge(tran_type='DR', tran_charge=1.50, create_date=datetime.datetime.now())
charges3 = TransactionCharge(tran_type='TR', tran_charge=1.0, create_date=datetime.datetime.now())
charges4 = TransactionCharge(tran_type='RTGS', tran_charge=5.0, create_date=datetime.datetime.now())
charges5 = TransactionCharge(tran_type='SF', tran_charge=3.0, create_date=datetime.datetime.now())
print("Basic Charges Created")
session.add(charges1)
session.add(charges2)
session.add(charges3)
session.add(charges4)
session.add(charges5)
session.commit()

acc1 = Account(acc_type='Savings', minbalance=0)
acc2 = Account(acc_type='Current', minbalance=5)
acc3 = Account(acc_type='Corporate', minbalance=100)
print("Account types created")
session.add(acc1)
session.add(acc2)
session.add(acc3)
session.commit()

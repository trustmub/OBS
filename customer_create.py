import random
import time

from src import db
from src.functions.genarators import Auto
from src.functions.transactions import AccountTransaction
from src.models.account_type_model import AccountType
from src.models.customer_model import Customer


def create_random_users():
    b = 0
    count = 0
    while b < 20:
        bee = str(b)
        name = "Customer" + bee

        acctrand = random.randint(1, 4)
        acct = db.session.query(AccountType).filter_by(id=acctrand).first()
        new_account = Auto().account_number_generator()
        rand_amount = random.randint(5, 10)
        record = Customer(first_name=name,
                          last_name=name,
                          dob=time.strftime('%Y-%m-%d'),
                          address="Address" + bee,
                          country='zimbabwe',
                          email="Customer" + bee + "@obs.co.zw",
                          gender='Male',
                          contact_number='',
                          working_bal=rand_amount,
                          acc_number=new_account,
                          account_type=acct.acc_type,
                          inputter_id=1)
        db.session.add(record)

        db.session.commit()
        # login_session['username'] = 'systemuser@obs.com'
        result = AccountTransaction(time.strftime('%Y-%m-%d'), rand_amount, new_account).create_account()
        if result == 1:
            print("Customer Number {} has been created successfully for account number {}".format(b, new_account))
        else:
            print("Account Creation Failed")
        # TransactionUpdate.accCreationCash(time.strftime('%Y-%m-%d'), rand_amount, new_account)
        b += 1


create_random_users()

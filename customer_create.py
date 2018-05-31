from views.customer import *
import threading


def create_random_users():
    b = 500
    count = 0
    while b < 500_000:
        bee = str(b)
        name = "Customer" + bee

        acctrand = random.randint(1, 4)
        acct = session.query(Account).filter_by(id=acctrand).first()
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
                          create_date=datetime.datetime.now(),
                          inputter_id=1)
        session.add(record)

        session.commit()
        result = AccountTransaction(time.strftime('%Y-%m-%d'), rand_amount, new_account).create_account()
        if result == 1:
            print("Customer Number {} has been created successfully for account number {}".format(b, new_account))
        else:
            print("Account Creation Failed")
        # TransactionUpdate.accCreationCash(time.strftime('%Y-%m-%d'), rand_amount, new_account)
        b += 1


create_random_users()

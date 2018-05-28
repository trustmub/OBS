from views.customer import *

b = 4

while b < 20:
    bee = str(b)
    name = "Customer" + bee

    acctrand = random.randint(1, 4)
    acct = session.query(Account).filter_by(id=acctrand).first()
    new_account = Auto.accountNumGen()
    rand_amount = random.randint(5, 10)
    record = Customer(first_name="Customer" + str(b) + "",
                      last_name=name,
                      dob=time.strftime('%Y-%m-%d'),
                      address="Address" + str(b),
                      country='zimbabwe',
                      email="Customer" + str(b) + "@obs.co.zw",
                      gender='Male',
                      contact_number='',
                      working_bal=rand_amount,
                      acc_number=new_account,
                      account_type=acct.acc_type,
                      create_date=datetime.datetime.now(),
                      inputter_id=1)
    session.add(record)
    session.commit()
    print("Customer Number {} has been created successfully for account number {}".format(b, new_account))
    # TransactionUpdate.accCreationCash(time.strftime('%Y-%m-%d'), rand_amount, new_account)
    AccountTransaction(time.strftime('%Y-%m-%d'), rand_amount, new_account).create_account()

    b += 1

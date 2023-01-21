"""
    controller.customer
    ---------------

    A customer controller that provide functionality for the customer creation and
    amendment my a back office personnel.

    this controller interacts with the user views.customer module
"""
import datetime

from src import db
# from src.models import session
from src.models.customer_model import Customer


# from src.models.models import Customer


class CustomerController:

    def __init__(self, first_name, last_name, dob, gender, contact_number, email, address, country, new_account,
                 working_bal, account_type, inputter_id):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.contact_number = contact_number
        self.email = email
        self.address = address
        self.country = country
        self.acc_account = new_account
        self.working_bal = working_bal
        self.account_type = account_type
        self.inputter_id = inputter_id

    def create_customer(self):
        new_client = Customer(first_name=self.first_name,
                              last_name=self.last_name,
                              dob=self.dob,
                              gender=self.gender,
                              contact_number=self.contact_number,
                              email=self.email,
                              address=self.address,
                              country=self.country,
                              acc_number=self.acc_account,
                              working_bal=self.working_bal,
                              account_type=self.account_type,
                              create_date=datetime.datetime.now(),
                              inputter_id=self.inputter_id)
        db.session.add(new_client)
        db.session.commit()

    def amend_customer(self):
        pass

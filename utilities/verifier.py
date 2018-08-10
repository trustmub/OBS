from cob.log_module import SystemOBS
from functions.genarators import Getters
from models import session
from models.models import Customer, User


class Verify:

    def __init__(self):
        self.verify_logging = SystemOBS().start_logging

    def account_exists(self, account_number):
        self.verify_logging("Account Verification " + account_number)
        record = session.query(Customer).filter_by(acc_number=account_number).first()
        if record is not None:
            return True

    def email_exists(self, email):
        self.verify_logging("Email Verification " + email)
        record = session.query(User).filter_by(email=email).first()
        if record is not None:
            self.verify_logging("Email Verification " + email + " FOUND")
            return True

    def till_is_linked(self, email):
        self.verify_logging("Till account Linked to :  " + email)
        record = session.query(User).filter_by(email=email).first()
        till_list = [i.user_id for i in Getters.getAllTellers()]
        if record.uid in till_list:
            return True

from src.cob.log_module import SystemOBS
from src.functions.genarators import Getters
from src.models import session
from src.models.models import Customer, User


class Verify:
    # def __init__(self):
    #     self.verify_logging = SystemOBS().start_logging

    _v_logging = SystemOBS.start_logging

    @classmethod
    def _account_exists(cls, account_number):
        cls._v_logging("Account Verification " + str(account_number))
        record = session.query(Customer).filter_by(acc_number=account_number).first()
        if record is not None:
            return True

    @classmethod
    def account_exists(cls, account_number):
        cls._v_logging("Account Verification " + str(account_number))
        record = session.query(Customer).filter_by(acc_number=account_number).first()
        if record is not None:
            return True

    @classmethod
    def email_exists(cls, email):
        cls._v_logging("Email Verification " + email)
        record = session.query(User).filter_by(email=email).first()
        if record is not None:
            cls._v_logging("Email Verification " + email + " FOUND")
            return True

    @classmethod
    def till_is_linked(cls, email):
        cls._v_logging("Till account Linked to :  " + email)
        record = session.query(User).filter_by(email=email).first()
        till_list = [i.user_id for i in Getters.getAllTellers()]
        if record.uid in till_list:
            return True

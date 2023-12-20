from src import db
from src.cob.log_module import SystemOBS
from src.utils.genarators import Getters
from src.models.customer_model import Customer
from src.models.system_user_model import SystemUser


class Verify:
    # def __init__(self):
    #     self.verify_logging = SystemOBS().start_logging

    _v_logging = SystemOBS.start_logging

    @classmethod
    def _account_exists(cls, account_number):
        cls._v_logging("Account Verification " + str(account_number))
        record = db.session.query(Customer).filter_by(acc_number=account_number).first()
        if record is not None:
            return True

    @classmethod
    def account_exists(cls, account_number):
        cls._v_logging("Account Verification " + str(account_number))
        record = db.session.query(Customer).filter_by(acc_number=account_number).first()
        if record is not None:
            return True

    @classmethod
    def email_exists(cls, email):
        cls._v_logging("Email Verification " + email)
        record = db.session.query(SystemUser).filter_by(email=email).first()
        if record is not None:
            cls._v_logging("Email Verification " + email + " FOUND")
            return True

    @classmethod
    def till_is_linked(cls, email):
        cls._v_logging("Till account Linked to :  " + email)
        record = db.session.query(SystemUser).filter_by(email=email).first()
        till_list = [i.user_id for i in Getters.getAllTellers()]
        if record.uid in till_list:
            return True

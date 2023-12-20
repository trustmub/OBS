from datetime import time

from sqlalchemy.exc import NoResultFound

from src.utils.Enums import TransactionType
from src.utils.genarators import TransactionUpdate, Getters
from src.models.customer_model import Customer
from src.models.system_user_model import SystemUser
from src.models.till_model import Till
from src import db


class TillRepository:

    @staticmethod
    def close_till(sys_balance):
        suspense = db.session.query(Customer).filter_by(account_type='suspense').first()
        TransactionUpdate.ttUpdate(
            TransactionType.CR_DR, sys_balance, time.strftime('%Y-%m-%d'),
            'Closing Balance',
            suspense.acc_number)

        till_detail = db.session.query(Till).filter_by(till_account=Getters.get_till_details().till_account).first()

        till_detail.c_balance = 0
        till_detail.o_balance = 0
        till_detail.user_id = ''
        db.session.add(till_detail)
        db.session.commit()
        # Credit suspense account with the closing balanced figure
        suspense.working_bal += sys_balance
        db.session.add(suspense)
        db.session.commit()

    @staticmethod
    def get_all_tills():
        return db.session.query(Till).all()

    @staticmethod
    def get_till_details_by_session(session_username:str):
        user_id = db.session.execute(db.select(SystemUser).filter_by(email=session_username)).scalar_one()
        try:
            return db.session.query(Till).filter_by(user_id=user_id).one()
        except NoResultFound:
            return None

    @staticmethod
    def get_till_details_by_user_id(user_id: int):
        try:
            return db.session.query(Till).filter_by(user_id=user_id).one()
        except NoResultFound:
            return None

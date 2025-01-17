# from . import session
# from src.models.models import Till
import datetime
import time

from flask import session

from src.utils.Enums import TransactionType
from src.utils.genarators import Getters, TransactionUpdate
from src.helpers.references import get_transaction_reference
from .. import db
from ..models.customer_model import Customer
from ..models.teller_transaction_model import TellerTransaction
from ..models.till_model import Till
from ..views.till_repository import TillRepository


class TillController(object):
    def __init__(
            self,
            branch_code,
            opening_balance,
            user_id,
            teller_id,
            remark='Teller Transfer',
            closing_balance=0):
        self.branch_code = branch_code
        self.opening_balance = opening_balance
        self.remark = remark
        self.user_id = user_id
        self.teller_id = teller_id
        self.closing_balance = closing_balance
        self._suspense_account = db.session.query(Customer).filter_by(account_type='suspense').first()

    def open_till(self):
        teller_record = db.session.query(Till).filter_by(id=self.teller_id).first()

        teller_record.branch_code = self.branch_code
        teller_record.opening_balance = self.opening_balance
        teller_record.closing_balance = self.closing_balance
        teller_record.remark = self.remark
        teller_record.date = time.strftime('%Y-%m-%d')
        teller_record.user_id = self.user_id

        db.session.add(teller_record)
        db.session.commit()

        # Perform till transaction
        teller_transaction = TellerTransaction(
            amount=self.opening_balance,
            date=time.strftime('%Y-%m-%d'),
            create_date=str(datetime.datetime.utcnow()),
            teller_id=self.teller_id,
            user_id=self.user_id,
            tran_type=TransactionType.CR_DR.value,
            tranref=get_transaction_reference()
        )
        db.session.add(teller_transaction)
        db.session.commit()

    # def close_till(self):
    #     till_detail = db.session.query(Till).filter_by(till_account=TillRepository.get_till_details_by_session(session["username"]).till_account).first()
    #
    #     TransactionUpdate.ttUpdate(
    #         TransactionType.CR_DR,
    #         till_detail.closing_balance,
    #         time.strftime('%Y-%m-%d'),
    #         'Closing Balance',
    #         self._suspense_account.acc_number
    #     )
    #     # Credit suspense account with the closing balanced figure
    #     self._suspense_account.working_bal += till_detail.closing_balance
    #     # reset the till position
    #     till_detail.closing_balance = 0
    #     till_detail.opening_balance = 0
    #     till_detail.user_id = 0
    #
    #     # commit Till and suspense account to Database
    #     db.session.add(till_detail)
    #     db.session.commit()
    #
    #     db.session.add(self._suspense_account)
    #     db.session.commit()

    def close_till(self):
        # Retrieve till details
        till_detail = db.session.query(Till).filter_by(till_account=TillRepository.get_till_details_by_session(session["username"]).till_account).first()

        # Update transaction
        TransactionUpdate.ttUpdate(
            TransactionType.CR_DR,
            till_detail.closing_balance,
            time.strftime('%Y-%m-%d'),
            'Closing Balance',
            self._suspense_account.acc_number
        )

        # Credit suspense account with the closing balance
        self._suspense_account.working_bal += till_detail.closing_balance

        # Reset the till position
        till_detail.closing_balance = 0
        till_detail.opening_balance = 0
        till_detail.user_id = 0

        # Commit Till and suspense account to Database
        db.session.add(till_detail)
        db.session.add(self._suspense_account)
        db.session.commit()

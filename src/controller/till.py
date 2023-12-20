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
    def __init__(self, branch_code,
                 o_balance,
                 user_id,
                 teller_id,
                 remark='Teller Transfer',
                 c_balance=0):
        self.branch_code = branch_code
        self.o_balance = o_balance
        self.remark = remark
        self.user_id = user_id
        self.teller_id = teller_id
        self.c_balance = c_balance
        self._suspense_account = db.session.query(Customer).filter_by(account_type='suspense').first()

    def open_till(self):
        # use teller_id to set the currency, till_account
        teller_record = db.session.query(Till).filter_by(id=self.teller_id).first()

        teller_record.branch_code = self.branch_code
        teller_record.o_balance = self.o_balance
        teller_record.c_balance = self.c_balance
        teller_record.till_account = teller_record.till_account
        teller_record.currency = teller_record.currency
        teller_record.remark = self.remark
        teller_record.date = time.strftime('%Y-%m-%d')
        # teller_record.create_date = datetime.datetime.now()
        teller_record.user_id = self.user_id

        db.session.add(teller_record)
        db.session.commit()

        # do a till transaction in crediting the till and affecting the volt Suspense account

        teller_transaction = TellerTransaction(amount=self.o_balance,
                                               date=time.strftime('%Y-%m-%d'),
                                               remark='',
                                               create_date=datetime.datetime.utcnow(),
                                               teller_id=self.teller_id,
                                               customer_id='',
                                               user_id=self.user_id,
                                               tran_type=TransactionType.CR_DR.value,
                                               tranref=get_transaction_reference())
        db.session.add(teller_transaction)
        db.session.commit()

        # TillController.ttUpdate(TransactionType.CR_DR, o_balance, time.strftime('%Y-%m-%d'), 'Teller Transfer',
        #                            suspense.acc_number)
        # ------------------------

        # Update the working balance of the suspense account
        # suspense.working_bal -= o_balance
        # session.add(suspense)
        # session.commit()
        # ---------------------------------------------------

    def close_till(self):
        till_detail = db.session.query(Till).filter_by(till_account=TillRepository.get_till_details_by_session(session["username"]).till_account).first()

        TransactionUpdate.ttUpdate(TransactionType.CR_DR, till_detail.c_balance, time.strftime('%Y-%m-%d'),
                                   'Closing Balance',
                                   self._suspense_account.acc_number)
        # Credit suspense account with the closing balanced figure
        self._suspense_account.working_bal += till_detail.c_balance
        # reset the till position
        till_detail.c_balance = 0
        till_detail.o_balance = 0
        till_detail.user_id = 0

        # commit Till and suspense account to Database
        db.session.add(till_detail)
        db.session.commit()

        db.session.add(self._suspense_account)
        db.session.commit()

        pass

    # def ttUpdate(t_type, amount, tran_date, tran_ref, acc_num):
    #     customer = session.query(Customer).filter_by(acc_number=acc_num).first()
    #     print("Till Details: {}".format(Getters.getTillDetails()))
    #     till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
    #
    #     tt = TellerTransactions(tran_type=t_type.value,  # CR or DR
    #                             tranref=Auto.reference_string_generator(),
    #                             amount=amount,
    #                             date=tran_date,
    #                             remark=tran_ref,
    #                             create_date=datetime.datetime.now(),
    #                             teller_id=till_detail.id,
    #                             customer_id=customer.custid,
    #                             user_id=Profile().user_details().uid)
    #     session.add(tt)
    #     session.commit()
    #
    #
    #
    #
    # till_record = session.query(Till).filter_by(id=self.till_num).first()
    #
    # till_record.branch_code = branch_code
    # till_record.o_balance = o_balance
    # till_record.user_id = user_id
    # till_record.date = time.strftime('%Y-%m-%d')
    #
    # session.add(till_record)
    # session.commit()

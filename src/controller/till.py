import time
from . import datetime
from . import session
from src.models.models import Till, Customer, TellerTransactions
from src.functions.transactions import CommitTransaction
from src.functions.Enums import TransactionType, TransactionMethod
from src.helpers.references import get_transaction_reference


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

    def open_till(self):
        # use teller_id to set the currency, till_account
        teller_record = session.query(Till).filter_by(id=self.teller_id).first()
        record = Till(branch_code=self.branch_code,
                      o_balance=self.o_balance,
                      c_balance=self.c_balance,
                      till_account=teller_record.till_account,
                      currency=teller_record.currency,
                      remark=self.remark,
                      date=time.strftime('%Y-%m-%d'),
                      create_date=datetime.now(),
                      user_id=self.user_id)
        session.add(record)
        session.commit()

        # do a till transaction in crediting the till and affecting the volt Suspense account

        teller_transaction = TellerTransactions(amount=self.o_balance,
                                                date=time.strftime('%Y-%m-%d'),
                                                remark='',
                                                create_date=datetime.utcnow(),
                                                teller_id=self.teller_id,
                                                customer_id='',
                                                user_id=self.user_id,
                                                tran_type=TransactionType.CR_DR.value,
                                                tranref=get_transaction_reference())

        TransactionUpdate.ttUpdate(TransactionType.CR_DR, o_balance, time.strftime('%Y-%m-%d'), 'Teller Transfer',
                                   suspense.acc_number)
        # ------------------------

        # Update the working balance of the suspense account
        suspense.working_bal -= o_balance
        session.add(suspense)
        session.commit()
        # ---------------------------------------------------


"""
    def ttUpdate(t_type, amount, tran_date, tran_ref, acc_num):
        customer = session.query(Customer).filter_by(acc_number=acc_num).first()
        print("Till Details: {}".format(Getters.getTillDetails()))
        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()

        tt = TellerTransactions(tran_type=t_type.value,  # CR or DR
                                tranref=Auto.reference_string_generator(),
                                amount=amount,
                                date=tran_date,
                                remark=tran_ref,
                                create_date=datetime.datetime.now(),
                                teller_id=till_detail.id,
                                customer_id=customer.custid,
                                user_id=Profile().user_details().uid)
        session.add(tt)
        session.commit()




    till_record = session.query(Till).filter_by(id=till_num).first()

    till_record.branch_code = branch_code
    till_record.o_balance = o_balance
    till_record.user_id = user_id
    till_record.date = time.strftime('%Y-%m-%d')

    session.add(till_record)
    session.commit()
"""

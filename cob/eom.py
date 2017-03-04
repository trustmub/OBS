# This is where all End of Month procedures are done

import random
import time
import datetime
import os

from flask import flash, session as login_session
from sqlalchemy.orm import sessionmaker

from models import *
from functions.genarators import *

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class AccountsEom:
    @staticmethod
    def accountInterestEom():
        # Calculates the total interest for each account in the interest table
        # Credits the account with the interest credits the interests account
        # update the transaction table appropriately
        sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        mo = sys_date.strftime('%m')
        all_accounts = session.query(Customer).all()
        for i in all_accounts:
            account = i.acc_number
            selector = session.query(Interest).filter_by(account=account).filter(
                extract('month', Interest.date) == mo).all()
            total = 0
            for x in selector:
                total += x.interest_earned
            i.working_bal += round(total, 2)
            session.add(i)
            session.commit()
            TransactionUpdate.accInterestUpdate(account, total, i.working_bal, i.custid)
        new = CobDates(date=sys_date,
                       process='ai',
                       status=1,
                       create_date=datetime.datetime.now())

        session.add(new)
        session.commit()
        pass

    @staticmethod
    def serviceFeesEom():
        if Getters.getCobDates(Getters.getSysDate().date):
            if session.query(CobDates).filter_by(process='sf').filter_by(status=1):
                print("service process skipped")
                pass
            else:
                pass
        else:
            charge = session.query(TransactionCharge).filter_by(tran_type='SF').first()
            all_accounts = session.query(Customer).all()
            for i in all_accounts:
                if i.contact_number == '09100000':
                    print("account passed")
                    pass
                else:
                    account = i.acc_number
                    # record = session.query(Customer).filter_by(acc_number=account).first()
                    # update an EOM transaction update
                    TransactionUpdate.eomServfeeTransactionUpdate(account, Getters.getSysDate().date, charge.tran_charge)
                    print("Transaction updated " + str(account) + " " + str(charge.tran_charge) + " " + str(Getters.getSysDate().date) + " record effected")
                    TransactionUpdate.accChargeUpdate('SF', account, Getters.getSysDate().date)
                    print("Charge effected")
            new = CobDates(date=Getters.getSysDate().date,
                           process='sf',
                           status=1,
                           create_date=datetime.datetime.now())
            session.add(new)
            session.commit()
            pass

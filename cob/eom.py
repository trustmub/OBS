# This is where all End of Month procedures are structured

import random
import time
import datetime
import os

from flask import flash, session as login_session
from sqlalchemy.orm import sessionmaker

from functions.Enums import TransactionType
from functions.transactions import ChargeTransaction
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
        if session.query(CobDates).filter_by(date=sys_date).filter_by(process='ai').first():
            print("Account interest has already run")
        else:
            for i in all_accounts:
                account = i.acc_number
                selector = session.query(Interest).filter_by(account=account).filter(
                    extract('month', Interest.date) == mo).all()
                total = 0
                for x in selector:
                    total += round(x.interest_earned, 2)
                tot = round(total, 2)
                i.working_bal += tot
                print("Account {} working balance upadated".format(i.working_bal))
                session.add(i)
                session.commit()
                TransactionUpdate.accInterestUpdate(account, tot, i.working_bal, i.custid)
                print("Account interest updated for Account {} Amount: ${} working balance now ${}".format(account, tot, i.working_bal))
            new = CobDates(date=sys_date,
                           process='ai',
                           status=1,
                           create_date=datetime.datetime.now())
            print("Cob Process for Account Interest done")
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
                print("Effect the process table")
                pass
        else:
            charge = session.query(TransactionCharge).filter_by(tran_type='SF').first()
            all_accounts = session.query(Customer).all()
            for i in all_accounts:
                if i.contact_number == '09100000' or i.account_type == 'Student':
                    print("account {} passed. Account Type is {}".format(i.acc_number, i.account_type))
                    pass
                else:
                    account = i.acc_number
                    # record = session.query(Customer).filter_by(acc_number=account).first()
                    # update an EOM transaction update
                    TransactionUpdate.eomServfeeTransactionUpdate(account, Getters.getSysDate().date, charge.tran_charge)
                    print("Transaction updated " + str(account) + " " + str(charge.tran_charge) + " " + str(Getters.getSysDate().date) + " record effected")
                    # TransactionUpdate.accChargeUpdate('SF', account, Getters.getSysDate().date)
                    ChargeTransaction(Getters.getSysDate().date, account).charges(TransactionType.SERVICE_FEE)
                    print("Charge effected for account {}".format(account))
            new = CobDates(date=Getters.getSysDate().date,
                           process='sf',
                           status=1,
                           create_date=datetime.datetime.now())
            session.add(new)
            session.commit()
            print("Process table updated")
            pass

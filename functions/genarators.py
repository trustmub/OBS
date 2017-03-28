import datetime
import logging
import random
import time

import os

from flask import flash, session as login_session
from sqlalchemy.orm import sessionmaker

from models import *

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# logging.basicConfig(filename="logs/system" + str(Getters.getSysDate().date) + ".log", level=logging.DEBUG)


class Getters:
    @staticmethod
    def getTransactionType():
        trantype = session.query(TransactionCharge).all()
        return trantype

    @staticmethod
    def getAllUsers():
        pass

    @staticmethod
    def getAvailableTellers():
        teller = session.query(Till).filter_by(user_id='').all()
        return teller

    @staticmethod
    def getAllTellers():
        teller = session.query(Till).all()
        return teller

    @staticmethod
    def getTillDetails():
        x = []
        for i in Getters.getAllTellers():
            x = x + [i.id]
        if Nav.userDetails().uid in x:
            till = session.query(Till).filter_by(user_id=Nav.userDetails().uid).first()
            return till
        else:
            till = []
            return till

    @staticmethod
    def getTellerStatus():
        alltills = session.query(Till).all()
        mylist = []
        for i in alltills:
            mylist = mylist + [i.user_id]
            # logging.info("user ID : {} added on the list".format(i.user_id))
        if Nav.userDetails().uid in mylist:
            return 1

    @staticmethod
    def getTellerWithdrawal():
        today = Getters.getSysDate().date
        # Get all transactions by current teller for today with credits
        total = 0
        if Getters.getTillDetails() is not None:
            my_till_trans = session.query(TellerTransactions).filter_by(
                teller_id=Getters.getTillDetails().id).filter_by(date=today).filter_by(tran_type='CR').filter(
                TellerTransactions.remark != 'Teller Transfer').all()

            for i in my_till_trans:
                total += i.amount
                # logging.info("Total Amount for {} is ()".format(my_till_trans.customer_id, total))
            return total
        else:
            return total

    @staticmethod
    def getTellerDeposits():
        today = Getters.getSysDate().date
        # Get all transactions by current teller for today with debits
        total = 0
        if Getters.getTillDetails() is not None:
            my_till_trans = session.query(TellerTransactions).filter_by(
                teller_id=Getters.getTillDetails().id).filter_by(date=today).filter_by(tran_type='DR').all()
            total = 0
            for i in my_till_trans:
                total += i.amount
            return total
        else:
            return total

    @staticmethod
    def getTellerTransactions():
        date = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
        if Getters.getTillDetails() is None:
            all_records = []
            return all_records
        else:
            all_records = session.query(TellerTransactions).filter_by(user_id=Nav.userDetails().uid).filter_by(
                date=date).all()
            return all_records

    @staticmethod
    def getAllTts():
        dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
        all_trans = session.query(TellerTransactions).filter_by(date=dt).all()
        return all_trans

    @staticmethod
    def getAccountType():
        record = session.query(Account).all()
        return record

    @staticmethod
    def getCustomerAccountDetails(acc_number):
        record = session.query(Customer).filter_by(acc_number=acc_number).first()
        return record

    @staticmethod
    def getBranch():
        branch = session.query(Branch).all()
        return branch

    @staticmethod
    def getCurrency():
        currency = session.query(Currency).all()
        return currency

    @staticmethod
    def getBanks():
        banks = session.query(Banks).all()
        return banks

    # End of business getters
    @staticmethod
    def getCobDates(date):
        cob_dates = session.query(CobDates).all()
        my_list = []
        for i in cob_dates:
            my_list += [i.date]
        if date in my_list:
            return True

    @staticmethod
    def getSysDate():
        record = session.query(SysDate).first()
        return record

    @staticmethod
    def getEodProcess(process):
        cob_process = session.query(CobDates).all()
        return cob_process

    @staticmethod
    def getTransactionDetails(ref):
        record = session.query(Transactions).filter_by(tranref=ref).first()
        return record


class TransactionUpdate:
    @staticmethod
    def accCreationCash(date, amount, acc_num):
        # establish the account for account creation
        acc_creation_sus_acc = session.query(Customer).filter_by(account_type='acccreate').first()

        cus = session.query(Customer).filter_by(acc_number=acc_num).one()
        # Update transactions Table
        trans = Transactions(trantype='CR',
                             tranref=Auto.referenceStringGen(),
                             tranmethod='Cash',
                             tran_date=date,
                             cheque_num='None',
                             acc_number=acc_creation_sus_acc.acc_number,
                             cr_acc_number=acc_num,
                             amount=amount,
                             current_balance=round(amount, 2),
                             remark='Account Creation',
                             custid=cus.custid,
                             create_date=datetime.datetime.now())
        session.add(trans)
        session.commit()

        # update the Account creation Suspanse Account
        acc_creation_sus_acc.working_bal -= amount
        session.add(acc_creation_sus_acc)
        session.commit()
        # ---------------------------------------------

        pass

    @staticmethod
    def depositTransactionUpdate(tran_date, acc_number, amount, tranref):
        customer = session.query(Customer).filter_by(acc_number=acc_number).one()
        current_balance = float(amount) + float(customer.working_bal)

        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        trans = Transactions(trantype='CR',
                             tranref=Auto.referenceStringGen(),
                             tranmethod='Cash',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=int(till_detail.till_account),
                             cr_acc_number=int(acc_number),
                             amount=amount,
                             current_balance=round(current_balance, 2),
                             remark='Deposit ' + tranref,
                             custid=customer.custid,
                             create_date=datetime.datetime.now())
        session.add(trans)
        session.commit()
        # Update customer working balance
        customer.working_bal = round(current_balance, 2)
        session.add(customer)
        session.commit()
        # -------------------------------

        # Update Till Opening/Closing   Balance
        till_detail.c_balance -= round(float(amount), 2)
        session.add(till_detail)
        session.commit()
        # ---------------------------
        pass

    @staticmethod
    def withdrawalTransactionUpdate(tran_date, acc_number, amount, tranref):
        #   1. withdrawal detail between customer and till
        customer = session.query(Customer).filter_by(acc_number=acc_number).one()
        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        cb = float(customer.working_bal) - float(amount)
        trans = Transactions(trantype='DR',
                             tranref=tranref,
                             tranmethod='Cash',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=int(acc_number),
                             cr_acc_number=int(till_detail.till_account),
                             amount=amount,
                             current_balance=round(cb, 2),
                             remark='Withdrawal ' + tranref,
                             custid=customer.custid,
                             create_date=datetime.datetime.now())
        session.add(trans)
        session.commit()
        # update customer working balance
        customer.working_bal = round(cb, 2)
        session.add(customer)
        session.commit()
        # -------------------------------
        # Update Till Opening/Closing balance
        till_detail.c_balance += round(amount, 2)
        session.add(till_detail)
        session.commit()
        # -------------------------------

        # 2. charge details between customer and charge account
        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = session.query(TransactionCharge).filter_by(tran_type='DR').first()
        cb2 = float(customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transactions(trantype='DR',
                              tranref=Auto.referenceStringGen(),
                              tranmethod='Charge Transfer',
                              tran_date=tran_date,
                              cheque_num='None',
                              acc_number=int(acc_number),
                              cr_acc_number=int(charge_account.acc_number),
                              amount=float(get_charge.tran_charge),
                              current_balance=round(cb2, 2),
                              remark='Debit Charge',
                              custid=customer.custid,
                              create_date=datetime.datetime.now())
        session.add(trans2)
        session.commit()

        # Update Working balance on charge
        customer.working_bal = round(cb2, 2)
        session.add(customer)
        session.commit()
        # ---------------------------------
        pass

    @staticmethod
    def transferTransactionUpdate(from_acc, to_acc, amount, remark, tran_date):
        f_customer = Getters.getCustomerAccountDetails(from_acc)
        current_balance = f_customer.working_bal - float(amount)
        # transaction reference for this transaction is the same since its one transaction
        tranref = Auto.referenceStringGen()
        # transaction for a from customer
        trans = Transactions(trantype='TR',
                             tranref=tranref,
                             tranmethod='Transfer',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=from_acc,
                             cr_acc_number=to_acc,
                             amount=amount,
                             current_balance=round(current_balance, 2),
                             remark='Transfer ' + remark,
                             custid=f_customer.custid,
                             create_date=datetime.datetime.now())

        session.add(trans)
        session.commit()

        # update from account working balance
        f_customer.working_bal = round(current_balance, 2)
        session.add(f_customer)
        session.commit()
        # -----------------------------------
        # updating To Account working balance
        to_customer = Getters.getCustomerAccountDetails(to_acc)
        to_customer.working_bal += round(amount, 2)
        session.add(to_customer)
        session.commit()
        # -----------------------------------
        # transaction for a to customer
        trans_to = Transactions(trantype='TR',
                                tranref=tranref,
                                tranmethod='Transfer',
                                tran_date=tran_date,
                                cheque_num='None',
                                acc_number=from_acc,
                                cr_acc_number=to_acc,
                                amount=amount,
                                current_balance=round(to_customer.working_bal, 2),
                                remark='Transfer ' + remark,
                                custid=to_customer.custid,
                                create_date=datetime.datetime.now()
                                )
        session.add(trans_to)
        session.commit()
        # charge details between customer and charge account

        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = session.query(TransactionCharge).filter_by(tran_type='TR').first()
        cb2 = float(f_customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transactions(trantype='DR',
                              tranref=Auto.referenceStringGen(),
                              tranmethod='Charge Transfer',
                              tran_date=tran_date,
                              cheque_num='None',
                              acc_number=int(from_acc),
                              cr_acc_number=int(charge_account.acc_number),
                              amount=float(get_charge.tran_charge),
                              current_balance=round(cb2, 2),
                              remark='Debit Charge',
                              custid=f_customer.custid,
                              create_date=datetime.datetime.now())
        session.add(trans2)
        session.commit()

        # update working balance of From Account after Charge effected
        f_customer.working_bal = round(cb2, 2)
        session.add(f_customer)
        session.commit()
        # -----------------------------------------------------------
        pass

    @staticmethod
    def externalTransferTransactionUpdate(from_acc, to_acc, amount, remark, tran_date):
        f_customer = Getters.getCustomerAccountDetails(from_acc)
        current_balance = f_customer.working_bal - float(amount)
        # same transaction reference between from account and suspence account
        tranref = Auto.referenceStringGen()
        # transaction for a from customer
        trans = Transactions(trantype='RTGS',
                             tranref=tranref,
                             tranmethod='Transfer',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=from_acc,
                             cr_acc_number=to_acc,
                             amount=amount,
                             current_balance=round(current_balance, 2),
                             remark='RTGS ' + remark,
                             custid=f_customer.custid,
                             create_date=datetime.datetime.now())

        session.add(trans)
        session.commit()

        # update from account working balance
        f_customer.working_bal = round(current_balance, 2)
        session.add(f_customer)
        session.commit()
        # -----------------------------------
        # updating RTGS Suspense Account Working balance
        to_suspense = session.query(Customer).filter_by(account_type='rtgs').first()
        to_suspense.working_bal += round(amount, 2)
        session.add(to_suspense)
        session.commit()
        # -----------------------------------
        # transaction for the Suspense Account
        trans_to = Transactions(trantype='RTGS',
                                tranref=tranref,
                                tranmethod='Transfer',
                                tran_date=tran_date,
                                cheque_num='None',
                                acc_number=from_acc,
                                cr_acc_number=to_acc,
                                amount=amount,
                                current_balance=round(to_suspense.working_bal, 2),
                                remark='RTGS ' + remark,
                                custid=to_suspense.custid,
                                create_date=datetime.datetime.now()
                                )
        session.add(trans_to)
        session.commit()
        # charge details between customer and charge account

        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        get_charge = session.query(TransactionCharge).filter_by(tran_type='RTGS').first()
        cb2 = float(f_customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transactions(trantype='DR',
                              tranref=Auto.referenceStringGen(),
                              tranmethod='Charge RTGS',
                              tran_date=tran_date,
                              cheque_num='None',
                              acc_number=int(from_acc),
                              cr_acc_number=int(charge_account.acc_number),
                              amount=float(get_charge.tran_charge),
                              current_balance=round(cb2, 2),
                              remark='RTGS Charge',
                              custid=f_customer.custid,
                              create_date=datetime.datetime.now())
        session.add(trans2)
        session.commit()

        # update working balance of From Account after Charge effected
        f_customer.working_bal = round(cb2, 2)
        session.add(f_customer)
        session.commit()
        # -----------------------------------------------------------
        pass

    @staticmethod
    def accInterestUpdate(cr_acc, total_amount, cb, cust_id):
        dr_acc_record = session.query(Customer).filter_by(account_type='interest').first()
        trans2 = Transactions(trantype='CR',
                              tranref=Auto.referenceStringGen(),
                              tranmethod='Interest',
                              tran_date=Getters.getSysDate().date,
                              cheque_num='None',
                              acc_number=int(dr_acc_record.acc_number),  # interest account
                              cr_acc_number=int(cr_acc),  # Client account
                              amount=float(total_amount),
                              current_balance=round(cb, 2),
                              remark='Interest',
                              custid=cust_id,
                              create_date=datetime.datetime.now())

        session.add(trans2)
        session.commit()
        pass

    @staticmethod
    def eomServfeeTransactionUpdate(acc_number, tran_date, amount):

        charged_customer = session.query(Customer).filter_by(acc_number=acc_number).first()
        current_balance = charged_customer.working_bal - amount

        servfee = session.query(Customer).filter_by(account_type='servfee').first()
        # same transactiion reference for customer and suspense account
        tranref = Auto.referenceStringGen()
        # transaction for Charged Customer
        trans = Transactions(trantype='SF',
                             tranref=tranref,
                             tranmethod='COB',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=acc_number,
                             cr_acc_number=servfee.acc_number,
                             amount=amount,
                             current_balance=round(current_balance, 2),
                             remark='SERVFEES',
                             custid=charged_customer.custid,
                             create_date=datetime.datetime.now())
        session.add(trans)
        session.commit()

        # update customer working balance
        charged_customer.working_bal = round(current_balance, 2)
        session.add(charged_customer)
        session.commit()
        # -------------------------------

        # transaction for Suspense account
        cb = servfee.working_bal + amount
        trans_sus = Transactions(trantype='SF',
                                 tranref=tranref,
                                 tranmethod='COB',
                                 tran_date=tran_date,
                                 cheque_num='None',
                                 acc_number=acc_number,
                                 cr_acc_number=servfee.acc_number,
                                 amount=amount,
                                 current_balance=round(cb, 2),
                                 remark='SERVFEES',
                                 custid=servfee.custid,
                                 create_date=datetime.datetime.now())

        session.add(trans_sus)
        session.commit()

        # update Suspence account Working balance
        servfee.working_bal = cb
        session.add(servfee)
        session.commit()
        # ---------------------------------------

        pass

    @staticmethod
    def ttUpdate(t_type, amount, tran_date, tran_ref, acc_num):
        customer = session.query(Customer).filter_by(acc_number=acc_num).first()
        till_detail = session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()

        tt = TellerTransactions(tran_type=t_type,  # CR or DR
                                tranref=Auto.referenceStringGen(),
                                amount=amount,
                                date=tran_date,
                                remark=tran_ref,
                                create_date=datetime.datetime.now(),
                                teller_id=till_detail.id,
                                customer_id=customer.custid,
                                user_id=Nav.userDetails().uid
                                )
        session.add(tt)
        session.commit()
        pass

    @staticmethod
    def getTransationTypeCharge():
        tt = session.query(TransactionCharge).all()
        return tt

    @staticmethod
    def accChargeUpdate(tran_type, acc_num, date):

        get_charge = session.query(TransactionCharge).filter_by(tran_type=tran_type).first()

        charge_account = session.query(Customer).filter_by(account_type='charges').first()
        servfee = session.query(Customer).filter_by(account_type='servfee').first()

        if tran_type == 'DR':
            new = ChargeTransactionTable(
                tran_type=tran_type,
                dr_account=acc_num,
                cr_account=charge_account.acc_number,
                charge=get_charge.tran_charge,
                date=date,
                create_date=datetime.datetime.now()
            )
            session.add(new)
            session.commit()
            # Update charge account working balance
            charge_account.working_bal += get_charge.tran_charge
            session.add(charge_account)
            session.commit()

        elif tran_type == 'SF':
            new = ChargeTransactionTable(
                tran_type=tran_type,
                dr_account=acc_num,
                cr_account=servfee.acc_number,
                charge=get_charge.tran_charge,
                date=date,
                create_date=datetime.datetime.now()
            )
            session.add(new)
            session.commit()
            # Update charge account working balance
            servfee.working_bal += get_charge.tran_charge
            session.add(servfee)
            session.commit()

        elif tran_type == 'TR':
            new = ChargeTransactionTable(
                tran_type=tran_type,
                dr_account=acc_num,
                cr_account=charge_account.acc_number,
                charge=get_charge.tran_charge,
                date=date,
                create_date=datetime.datetime.now()
            )
            session.add(new)
            session.commit()
            # Update charge account working balance
            charge_account.working_bal += get_charge.tran_charge
            session.add(charge_account)
            session.commit()
        elif tran_type == 'RTGS':
            new = ChargeTransactionTable(
                tran_type=tran_type,
                dr_account=acc_num,
                cr_account=charge_account.acc_number,
                charge=get_charge.tran_charge,
                date=date,
                create_date=datetime.datetime.now()
            )
            session.add(new)
            session.commit()
            # Update charge account working balance
            charge_account.working_bal += get_charge.tran_charge
            session.add(charge_account)
            session.commit()
        else:
            pass

    @staticmethod
    def smartUpdate():
        # update the transaction table with
        # 1. withdrawal detail between customer and till
        # 2. charge details between customer and charge account
        # Effect the transaction
        # 1. between customer and till
        # 2. cutomer and charge account

        # update the charges table with charges information
        pass


class Auto:
    @staticmethod
    def accountNumGen():
        # Generates account numbers
        branch = str(33)
        acc_number = str(random.randint(111111, 999999))
        str_acc_num = branch + acc_number
        account_number = int(str_acc_num)
        mylist = []
        all_account = session.query(Customer).all()
        for i in all_account:
            mylist =mylist + [i.acc_number]
        if account_number in mylist:
            Auto.accountNumGen()
        else:
            return account_number


    @staticmethod
    def referenceStringGen():
        sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        time_component = sys_date.strftime("%y%m%d")
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        random.shuffle(alphabet)
        rand_string = random.sample(alphabet, 5)
        alp = "".join(rand_string)
        ref_str = "FT" + str(time_component) + alp.upper()
        mylist = []
        tr = session.query(Transactions).all()
        for i in tr:
            mylist = mylist + [i.tranref]
        if ref_str in mylist:
            Auto.referenceStringGen()
        else:
            return ref_str

    @staticmethod
    def systemAccNumberGen():
        branch = '33'
        currency = 'USD'
        acc = str(random.randint(11111111, 99999999))
        str_acc_number = branch + acc
        mylist = []
        all_account = session.query(Customer).all()
        for i in all_account:
            mylist =mylist + [i.acc_number]
        if int(str_acc_number) in mylist:
            Auto.systemAccNumberGen()
        else:
            return int(str_acc_number)


class Nav:
    @staticmethod
    def userDetails():
        usr = login_session['username']
        user = session.query(User).filter_by(email=usr).first()
        return user

    @staticmethod
    def messageDetails():
        pass

    @staticmethod
    def activityDetails():
        pass


class Checker:
    @staticmethod
    def accNumberChecker(acc_number):
        acc = int(acc_number)
        all_acc = session.query(Customer).all()
        acc_list = []
        for i in all_acc:
            acc_list = acc_list + [i.acc_number]
        if acc in acc_list:
            return True

    @staticmethod
    def userEmailChecker(email):
        user = session.query(User).all()
        user_list = []
        for i in user:
            user_list = user_list + [i.email]
        if email in user_list:
            return True

    @staticmethod
    def userDbSession(email):
        user = session.query(User).filter_by(email=email).first()
        if not user.lock:
            return False

    @staticmethod
    def userTillLink(email):
        user = session.query(User).filter_by(email=email).first()
        till_list = []
        for i in Getters.getAllTellers():
            till_list = till_list + [i.user_id]
        if user.uid in till_list:
            return True

    @staticmethod
    def eom_process_day():
        change_date = session.query(SysDate).first()
        today_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        add_day = datetime.timedelta(days=1)
        next_day = today_date + add_day
        if next_day.strftime('%m') == today_date.strftime('%m'):
            return False
        else:
            return True

    @staticmethod
    def is_weekday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

    @staticmethod
    def is_holiday():
        pass

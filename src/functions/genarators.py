import datetime
import random

from src import db
from src.functions.Enums import AccountTypes
from src.functions.user_profile import Profile
from src.models.account_type_model import AccountType
from src.models.bank_table_model import Banks
from src.models.branch_model import Branch
from src.models.currency_model import Currency
from src.models.customer_model import Customer
from src.models.system_cob_date_model import CobDates
from src.models.system_date_model import SysDate
from src.models.teller_transaction_model import TellerTransaction
from src.models.till_model import Till
from src.models.transaction_charge_fee_model import TransactionChargeFee
from src.models.transaction_model import Transaction


# logging.basicConfig(filename="logs/system" + str(Getters.getSysDate().date) + ".log", level=logging.DEBUG)


class Getters:
    @staticmethod
    def getTransactionType():
        return db.session.query(TransactionChargeFee).all()

    @staticmethod
    def getAllUsers():
        pass

    @staticmethod
    def getAvailableTellers():
        return db.session.query(Till).filter_by(user_id='').all()

    @staticmethod
    def getAllTellers():
        return db.session.query(Till).all()

    @staticmethod
    def getTillDetails():
        till_ids = [i.id for i in Getters.getAllTellers()]
        tellers = Getters.getAllTellers()
        user_id = Profile().user_details().uid
        print("Till IDs: {}".format(till_ids))
        print("Profile details id: {}".format(Profile().user_details().uid))
        for teller in tellers:
            if teller.user is not None:
                if user_id == teller.user.uid:
                    return db.session.query(Till).filter_by(user_id=user_id).first()

    @staticmethod
    def getTellerStatus():
        mylist = [i.user_id for i in db.session.query(Till).all()]
        if Profile().user_details().uid in mylist:
            return 1

    @staticmethod
    def getTellerWithdrawal():
        today = Getters.getSysDate().date
        # Get all transactions by current teller for today with credits
        total = 0
        if Getters.getTillDetails() is not None:
            print("This is the till details: {}".format(Getters.getTillDetails()))
            my_till_trans = db.session.query(TellerTransaction) \
                .filter_by(teller_id=Getters.getTillDetails().id) \
                .filter_by(date=today) \
                .filter_by(tran_type='CR') \
                .filter(TellerTransaction.remark != 'Teller Transfer') \
                .all()

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
            my_till_trans = db.session.query(TellerTransaction).filter_by(
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
            return []
        else:
            all_records = db.session.query(TellerTransaction).filter_by(
                user_id=Profile().user_details().uid).filter_by(
                date=date).all()
            return all_records

    @staticmethod
    def getAllTts():
        dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
        all_trans = db.session.query(TellerTransaction).filter_by(date=dt).all()
        return all_trans

    @staticmethod
    def getAccountType():
        return db.session.query(AccountType).all()

    @staticmethod
    def getCustomerAccountDetails(acc_number):
        return db.session.query(Customer).filter_by(acc_number=acc_number).first()

    @staticmethod
    def getBranch():
        return db.session.query(Branch).all()

    @staticmethod
    def getCurrency():
        return db.session.query(Currency).all()

    @staticmethod
    def getBanks():
        return db.session.query(Banks).all()

    # End of business getters
    @staticmethod
    def getCobDates(date):
        cob_dates = db.session.query(CobDates).all()
        my_list = []
        for i in cob_dates:
            my_list += [i.date]
        if date in my_list:
            return True

    @staticmethod
    def getSysDate():
        record = db.session.query(SysDate).first()
        return record

    @staticmethod
    def getEodProcess(process):
        cob_process = db.session.query(CobDates).all()
        return cob_process

    @staticmethod
    def getTransactionDetails(ref):
        record = db.session.query(Transaction).filter_by(tranref=ref).first()
        return record


class TransactionPersist:

    def __init__(self, date, acc_number, amount, suspence_account_type=AccountTypes.ACCOUNT_CREATION):
        self.date = date
        self.acc_number = acc_number
        self.amount = amount
        self._suspence_account_type = suspence_account_type
        self._suspence_account = db.session.query(Customer).filter_by(
            account_type=self.suspence_account_type.value).first()
        self._customer_account = db.session.query(Customer).filter_by(acc_number=self.acc_number).one()

    def deposit(self):
        account_creation_current_balance = round(self.amount, 2)

        transaction = Transaction(trantype='CR',
                                  tranref=Auto.reference_string_generator(),
                                  tranmethod='Cash',
                                  tran_date=self.date,
                                  cheque_num='None',
                                  acc_number=self._suspence_account.acc_number,
                                  cr_acc_number=self.acc_number,
                                  amount=self.amount,
                                  current_balance=round(self.amount, 2),
                                  remark='Account Creation',
                                  custid=self._customer_account.custid)
        db.session.add(transaction)
        db.session.commit()

    def withdrawal(self):
        pass

    def transfer(self):
        pass


class TransactionUpdate:
    @staticmethod
    def accCreationCash(date, amount, acc_num):
        # establish the account for account creation
        acc_creation_sus_acc = db.session.query(Customer).filter_by(account_type='acccreate').first()

        cus = db.session.query(Customer).filter_by(acc_number=acc_num).one()
        # Update transactions Table
        trans = Transaction(trantype='CR',
                            tranref=Auto.reference_string_generator(),
                            tranmethod='Cash',
                            tran_date=date,
                            cheque_num='None',
                            acc_number=acc_creation_sus_acc.acc_number,
                            cr_acc_number=acc_num,
                            amount=amount,
                            current_balance=round(amount, 2),
                            remark='Account Creation',
                            custid=cus.custid)
        db.session.add(trans)
        db.session.commit()

        # update the Account creation Suspanse Account
        acc_creation_sus_acc.working_bal -= amount
        db.session.add(acc_creation_sus_acc)
        db.session.commit()
        # ---------------------------------------------

        pass

    @staticmethod
    def depositTransactionUpdate(tran_date, acc_number, amount, tranref):
        customer = db.session.query(Customer).filter_by(acc_number=acc_number).one()
        current_balance = float(amount) + float(customer.working_bal)

        till_detail = db.session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        trans = Transaction(trantype='CR',
                            tranref=Auto.reference_string_generator(),
                            tranmethod='Cash',
                            tran_date=tran_date,
                            cheque_num='None',
                            acc_number=int(till_detail.till_account),
                            cr_acc_number=int(acc_number),
                            amount=amount,
                            current_balance=round(current_balance, 2),
                            remark='Deposit ' + tranref,
                            custid=customer.custid)
        db.session.add(trans)
        db.session.commit()
        # Update customer working balance
        customer.working_bal = round(current_balance, 2)
        db.session.add(customer)
        db.session.commit()
        # -------------------------------

        # Update Till Opening/Closing   Balance
        till_detail.c_balance -= round(float(amount), 2)
        db.session.add(till_detail)
        db.session.commit()
        # ---------------------------
        pass

    @staticmethod
    def withdrawalTransactionUpdate(tran_date, acc_number, amount, tranref):
        #   1. withdrawal detail between customer and till
        customer = db.session.query(Customer).filter_by(acc_number=acc_number).one()
        till_detail = db.session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()
        cb = float(customer.working_bal) - float(amount)
        trans = Transaction(trantype='DR',
                            tranref=tranref,
                            tranmethod='Cash',
                            tran_date=tran_date,
                            cheque_num='None',
                            acc_number=int(acc_number),
                            cr_acc_number=int(till_detail.till_account),
                            amount=amount,
                            current_balance=round(cb, 2),
                            remark='Withdrawal ' + tranref,
                            custid=customer.custid)
        db.session.add(trans)
        db.session.commit()
        # update customer working balance
        customer.working_bal = round(cb, 2)
        db.session.add(customer)
        db.session.commit()
        # -------------------------------
        # Update Till Opening/Closing balance
        till_detail.c_balance += round(amount, 2)
        db.session.add(till_detail)
        db.session.commit()
        # -------------------------------

        # 2. charge details between customer and charge account
        charge_account = db.session.query(Customer).filter_by(account_type='charges').first()
        get_charge = db.session.query(TransactionChargeFee).filter_by(tran_type='DR').first()
        cb2 = float(customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transaction(trantype='DR',
                             tranref=Auto.reference_string_generator(),
                             tranmethod='Charge Transfer',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=int(acc_number),
                             cr_acc_number=int(charge_account.acc_number),
                             amount=float(get_charge.tran_charge),
                             current_balance=round(cb2, 2),
                             remark='Debit Charge',
                             custid=customer.custid)
        db.session.add(trans2)
        db.session.commit()

        # Update Working balance on charge
        customer.working_bal = round(cb2, 2)
        db.session.add(customer)
        db.session.commit()
        # ---------------------------------

    @staticmethod
    def transferTransactionUpdate(from_acc, to_acc, amount, remark, tran_date):
        f_customer = Getters.getCustomerAccountDetails(from_acc)
        current_balance = f_customer.working_bal - float(amount)
        # transaction reference for this transaction is the same since its one transaction
        tranref = Auto.reference_string_generator()
        # transaction for a from customer
        trans = Transaction(trantype='TR',
                            tranref=tranref,
                            tranmethod='Transfer',
                            tran_date=tran_date,
                            cheque_num='None',
                            acc_number=from_acc,
                            cr_acc_number=to_acc,
                            amount=amount,
                            current_balance=round(current_balance, 2),
                            remark='Transfer ' + remark,
                            custid=f_customer.custid)

        db.session.add(trans)
        db.session.commit()

        # update from account working balance
        f_customer.working_bal = round(current_balance, 2)
        db.session.add(f_customer)
        db.session.commit()
        # -----------------------------------
        # updating To Account working balance
        to_customer = Getters.getCustomerAccountDetails(to_acc)
        to_customer.working_bal += round(amount, 2)
        db.session.add(to_customer)
        db.session.commit()
        # -----------------------------------
        # transaction for a to customer
        trans_to = Transaction(trantype='TR',
                               tranref=tranref,
                               tranmethod='Transfer',
                               tran_date=tran_date,
                               cheque_num='None',
                               acc_number=from_acc,
                               cr_acc_number=to_acc,
                               amount=amount,
                               current_balance=round(to_customer.working_bal, 2),
                               remark='Transfer ' + remark,
                               custid=to_customer.custid
                               )
        db.session.add(trans_to)
        db.session.commit()
        # charge details between customer and charge account

        charge_account = db.session.query(Customer).filter_by(account_type='charges').first()
        get_charge = db.session.query(TransactionChargeFee).filter_by(tran_type='TR').first()
        cb2 = float(f_customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transaction(trantype='DR',
                             tranref=Auto.reference_string_generator(),
                             tranmethod='Charge Transfer',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=int(from_acc),
                             cr_acc_number=int(charge_account.acc_number),
                             amount=float(get_charge.tran_charge),
                             current_balance=round(cb2, 2),
                             remark='Debit Charge',
                             custid=f_customer.custid)
        db.session.add(trans2)
        db.session.commit()

        # update working balance of From Account after Charge effected
        f_customer.working_bal = round(cb2, 2)
        db.session.add(f_customer)
        db.session.commit()
        # -----------------------------------------------------------
        pass

    @staticmethod
    def externalTransferTransactionUpdate(from_acc, to_acc, amount, remark, tran_date):
        f_customer = Getters.getCustomerAccountDetails(from_acc)
        current_balance = f_customer.working_bal - float(amount)
        # same transaction reference between from account and suspence account
        tranref = Auto.reference_string_generator()
        # transaction for a from customer
        trans = Transaction(trantype='RTGS',
                            tranref=tranref,
                            tranmethod='Transfer',
                            tran_date=tran_date,
                            cheque_num='None',
                            acc_number=from_acc,
                            cr_acc_number=to_acc,
                            amount=amount,
                            current_balance=round(current_balance, 2),
                            remark='RTGS ' + remark,
                            custid=f_customer.custid)

        db.session.add(trans)
        db.session.commit()

        # update from account working balance
        f_customer.working_bal = round(current_balance, 2)
        db.session.add(f_customer)
        db.session.commit()
        # -----------------------------------
        # updating RTGS Suspense Account Working balance
        to_suspense = db.session.query(Customer).filter_by(account_type='rtgs').first()
        to_suspense.working_bal += round(amount, 2)
        db.session.add(to_suspense)
        db.session.commit()
        # -----------------------------------
        # transaction for the Suspense Account
        trans_to = Transaction(trantype='RTGS',
                               tranref=tranref,
                               tranmethod='Transfer',
                               tran_date=tran_date,
                               cheque_num='None',
                               acc_number=from_acc,
                               cr_acc_number=to_acc,
                               amount=amount,
                               current_balance=round(to_suspense.working_bal, 2),
                               remark='RTGS ' + remark,
                               custid=to_suspense.custid
                               )
        db.session.add(trans_to)
        db.session.commit()
        # charge details between customer and charge account

        charge_account = db.session.query(Customer).filter_by(account_type='charges').first()
        get_charge = db.session.query(TransactionChargeFee).filter_by(tran_type='RTGS').first()
        cb2 = float(f_customer.working_bal) - float(get_charge.tran_charge)
        trans2 = Transaction(trantype='DR',
                             tranref=Auto.reference_string_generator(),
                             tranmethod='Charge RTGS',
                             tran_date=tran_date,
                             cheque_num='None',
                             acc_number=int(from_acc),
                             cr_acc_number=int(charge_account.acc_number),
                             amount=float(get_charge.tran_charge),
                             current_balance=round(cb2, 2),
                             remark='RTGS Charge',
                             custid=f_customer.custid)
        db.session.add(trans2)
        db.session.commit()

        # update working balance of From Account after Charge effected
        f_customer.working_bal = round(cb2, 2)
        db.session.add(f_customer)
        db.session.commit()
        # -----------------------------------------------------------
        pass

    @staticmethod
    def accInterestUpdate(cr_acc, total_amount, cb, cust_id):
        dr_acc_record = db.session.query(Customer).filter_by(account_type='interest').first()
        trans2 = Transaction(trantype='CR',
                             tranref=Auto.reference_string_generator(),
                             tranmethod='Interest',
                             tran_date=Getters.getSysDate().date,
                             cheque_num='None',
                             acc_number=int(dr_acc_record.acc_number),  # interest account
                             cr_acc_number=cr_acc,  # Client account
                             amount=float(total_amount),
                             current_balance=round(cb, 2),
                             remark='Interest',
                             custid=cust_id)

        db.session.add(trans2)
        db.session.commit()
        pass

    @staticmethod
    def eomServfeeTransactionUpdate(acc_number, tran_date, amount):
        charged_customer = db.session.query(Customer).filter_by(acc_number=acc_number).first()
        current_balance = charged_customer.working_bal - amount

        servfee = db.session.query(Customer).filter_by(account_type='servfee').first()
        # same transactiion reference for customer and suspense account
        tranref = Auto.reference_string_generator()
        # transaction for Charged Customer
        trans = Transaction(trantype='SF',
                            tranref=tranref,
                            tranmethod='COB',
                            tran_date=tran_date,
                            cheque_num='None',
                            acc_number=acc_number,
                            cr_acc_number=servfee.acc_number,
                            amount=amount,
                            current_balance=round(current_balance, 2),
                            remark='SERVFEES',
                            custid=charged_customer.custid)
        db.session.add(trans)
        db.session.commit()

        # update customer working balance
        charged_customer.working_bal = round(current_balance, 2)
        db.session.add(charged_customer)
        db.session.commit()
        # -------------------------------

        # transaction for Suspense account
        cb = servfee.working_bal + amount
        trans_sus = Transaction(trantype='SF',
                                tranref=tranref,
                                tranmethod='COB',
                                tran_date=tran_date,
                                cheque_num='None',
                                acc_number=acc_number,
                                cr_acc_number=servfee.acc_number,
                                amount=amount,
                                current_balance=round(cb, 2),
                                remark='SERVFEES',
                                custid=servfee.custid)

        db.session.add(trans_sus)
        db.session.commit()

        # update Suspence account Working balance
        servfee.working_bal = cb
        db.session.add(servfee)
        db.session.commit()
        # ---------------------------------------

        pass

    @staticmethod
    def ttUpdate(t_type, amount, tran_date, tran_ref, acc_num):
        """
        when a withdrawal or a deposit is done this is how the till is affected

        :param t_type:
        :param amount:
        :param tran_date:
        :param tran_ref:
        :param acc_num:
        :return:
        """
        customer = db.session.query(Customer).filter_by(acc_number=acc_num).first()
        print("Till Details: {}".format(Getters.getTillDetails()))
        till_detail = db.session.query(Till).filter_by(till_account=Getters.getTillDetails().till_account).first()

        tt = TellerTransaction(tran_type=t_type.value,  # CR or DR
                               tranref=Auto.reference_string_generator(),
                               amount=amount,
                               date=tran_date,
                               remark=tran_ref,
                               create_date=datetime.datetime.now(),
                               teller_id=till_detail.id,
                               customer_id=customer.custid,
                               user_id=Profile().user_details().uid)
        db.session.add(tt)
        db.session.commit()
        pass

    @staticmethod
    def getTransationTypeCharge():
        tt = db.session.query(TransactionChargeFee).all()
        return tt

    @staticmethod
    def smartUpdate():
        # update the transaction table with
        # 1. withdrawal detail between customer and till
        # 2. charge details between customer and charge account
        # Effect the transaction
        # 1. between customer and till
        # 2. customer and charge account

        # update the charges table with charges information
        pass


class Auto:

    def __init__(self):
        self.account_listing = db.session.query(Customer).all()

    def account_number_generator(self):
        # Generates account numbers
        branch = str(33)
        acc_number = str(random.randint(111111, 999999))
        str_acc_num = branch + acc_number
        account_number = int(str_acc_num)
        account_list = [i.acc_number for i in self.account_listing]
        if account_number in account_list:
            print("Duplicate found::::: Running again")
            self.account_number_generator()
        else:
            return account_number

    @staticmethod
    def reference_string_generator():
        sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        time_component = sys_date.strftime("%y%m%d")
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        random.shuffle(alphabet)
        rand_string = random.sample(alphabet, 5)
        alp = "".join(rand_string)
        ref_str = "FT" + str(time_component) + alp.upper()

        transaction_list = [i.tranref for i in db.session.query(Transaction).all()]

        if ref_str in transaction_list:
            Auto.reference_string_generator()
        else:
            return ref_str

    @staticmethod
    def system_account_number_generator():
        branch = '33'
        currency = 'USD'
        acc = str(random.randint(11111111, 99999999))
        str_acc_number = branch + acc
        mylist = [1]
        all_account = db.session.query(Customer).all()
        for i in all_account:
            mylist = mylist + [i.acc_number]
        if int(str_acc_number) in mylist:
            Auto.system_account_number_generator()
        else:
            return int(str_acc_number)


class Checker:

    @staticmethod
    def eom_process_day():
        # change_date = db.session.query(SysDate).first()
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

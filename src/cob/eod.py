# This is where End  Of Day procedures are done
import os
import time
from src.functions.genarators import *
from src.models import session
from src.cob.eom import AccountsEom

from src.models.models import Interest


class Accounts:
    def __init__(self):
        self.account_opening = os.path.abspath("src//reports//AccountsOpened" + Getters.getSysDate().date + ".csv")

    def accOpeningBalancing(self):
        print("Account Opening balancing")
        # Check all account opened today
        count = 0
        dt = Getters.getSysDate().date
        mo = time.strftime('%m')
        ma = datetime.datetime.month
        acc_opened = session.query(Transactions).filter_by(remark='Account Creation').filter_by(tran_date=dt).all()
        for i in acc_opened:
            count += float(i.amount)
        if acc_opened is not None:
            with open(self.account_opening, mode="w",
                      encoding="utf-8") as myFile:
                for i in acc_opened:
                    myFile.write(
                        str(i.trantype) + "," + i.tranref + "," + i.tranmethod + "," + str(i.tran_date) + "," + str(
                            i.cheque_num) + "," + str(i.acc_number) + "," + str(i.cr_acc_number) + "," + str(
                            i.amount) + "," + str(i.custid) + "\n")

            # update the account opening accordingly
        acc_opening_account = session.query(Customer).filter_by(account_type='acccreate').first()
        acc_opening_account.working_bal += count
        session.add(acc_opening_account)
        session.commit()
        # accumulate all opening balances for the new accounts
        # credit the ...acccreate.... account with the figure to zero it off
        # generate a report for all those account and the zeroing off process
        # create a list for all th entries being done
        pass

    @staticmethod
    def accountInterestEod():
        print("Account Interest")
        interest_per_annam = 0.05
        debit_interest = 0.15
        all_accounts = session.query(Customer).all()
        for i in all_accounts:
            date = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
            print("Interest for date: " + date)
            acc = i.acc_number
            print("Account picked is: " + str(acc))
            eod_bal = float(i.working_bal)
            print("Working balance is: " + str(eod_bal))
            if i.working_bal > 0:
                # interest charges on credit balances
                interest = (interest_per_annam / 365) * eod_bal
            else:
                # interest charged on negative balances
                interest = (debit_interest / 365) * eod_bal
            print("Interest Charges: " + str(interest))
            table_update = Interest(date=date,
                                    account=acc,
                                    eod_bal=round(eod_bal, 2),
                                    interest_earned=round(interest, 4))
            session.add(table_update)
            print("Record Account " + date + " || " + str(acc) + " || " + str(
                eod_bal) + " ==== daily interest ----" + str(interest) + " Updated on date : ----" + date)

        session.commit()
        print("Account interest Calculation complete")
        pass

        # check the closing balance for each account
        # calculates a daily interest for the account
        # populates the interest table with account number, interest for the day and date
        pass


class Reporting:

    def __init__(self):
        self.credit_transactions = os.path.abspath(
            "src//reports//CreditTransactions" + Getters.getSysDate().date + ".csv")

    @staticmethod
    def accountClosingBalances():
        # a report of all accounts and there closing balance for the day
        acc_list = session.query(Customer).all()
        dt = Getters.getSysDate().date  # .strftime("%Y-%m-%d")
        with open("src/reports/AccountClosingBalances" + str(dt) + ".txt", mode="w", encoding="utf-8") as myfile:
            for i in acc_list:
                myfile.write(str(i.acc_number) + " : " + str(i.working_bal) + "\n")
        pass

    @staticmethod
    def tellerTransactionReport():
        # report of all transactions done by each teller
        dt = Getters.getSysDate().date
        tt = Getters.getAllTts()
        with open("src/reports/TellerTransactions" + str(dt) + ".txt", mode="w", encoding="utf-8") as myfile:
            for i in tt:
                myfile.write(
                    str(i.id) + " : " + str(i.tran_type) + " : " + str(i.amount) + " : " + str(i.date) + " : " + str(
                        i.teller_id) + " : " + str(i.customer.acc_number) + " : " + str(i.user_id) + "\n")
        pass

    def creditTransactions(self):
        # all deposits done for the day
        record = session.query(Transactions).filter_by(tran_date=Getters.getSysDate().date).filter_by(
            trantype='CR').all()
        if record is not None:
            print("The number of records are " + str(len(record)))
            with open(self.credit_transactions, mode="w", encoding="utf-8") as myFile:
                skip_account = [33139793,
                                33139793,
                                33145826,
                                33145826,
                                33145826,
                                33145826,
                                33722073,
                                33202507,
                                33613681,
                                33407739]
                for i in record:
                    print("The record giving problems is" + str(i.cr_acc_number))
                    if i.cr_acc_number not in skip_account:
                        myFile.write(
                            str(i.trantype) + "," + i.tranref + "," + i.tranmethod + "," + str(i.tran_date) + "," + str(
                                i.cheque_num) + "," + str(i.acc_number) + "," + str(i.cr_acc_number) + "," + str(
                                i.amount) + "," + str(i.custid) + "\n")

        pass

    @staticmethod
    def dbsysdate():
        date_change = session.query(SysDate).first()
        mydate = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        add_day = datetime.timedelta(days=1)
        new_date = mydate + add_day
        date_change.date = new_date.strftime('%Y-%m-%d')
        session.add(date_change)
        session.commit()

    @staticmethod
    def debitTransactions():
        # all withdrawals done for the day on customer account
        record = session.query(Transactions).filter_by(tran_date=Getters.getSysDate().date).filter_by(
            trantype='DR').all()
        with open("src/reports/DebitTransactions" + Getters.getSysDate().date + ".csv", mode="w",
                  encoding="utf-8") as myFile:
            for i in record:
                myFile.write(
                    str(i.trantype) + "," + i.tranref + "," + i.tranmethod + "," + str(i.tran_date) + "," + str(
                        i.cheque_num) + "," + str(i.acc_number) + "," + str(i.cr_acc_number) + "," + str(
                        i.amount) + "," + str(i.custid) + "\n")

        pass

    @staticmethod
    def accountsOpenedReport():
        # lists all the accounts opened today
        pass


def eod_process():
    print("Accouts : Accounts Opening Balancing")
    Accounts().accOpeningBalancing()
    print("Account : Account Interest End Of Day")
    Accounts.accountInterestEod()
    print("Reporting : Creadit Transaction Report")
    Reporting().creditTransactions()
    print("Reporting : Debit Transaction Reports")
    Reporting.debitTransactions()
    print("Reports : Account Closing Balance")
    Reporting.accountClosingBalances()
    print("Reporting : Teller Transaction Reports")
    Reporting.tellerTransactionReport()


def eom_process():
    eod_process()
    print("Updating interest to Client accounts")
    AccountsEom.accountInterestEom()
    print("Service Fee charges")
    AccountsEom.serviceFeesEom()
    Reporting().creditTransactions()
    print("Reporting : Debit Transaction Reports")
    Reporting.debitTransactions()
    print("Reports : Account Closing Balance")
    Reporting.accountClosingBalances()


def main():
    mydate = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
    d_year = mydate.year
    d_month = mydate.month
    d_day = mydate.day
    md = datetime.date(int(d_year), int(d_month), int(d_day))
    if Checker.is_weekday(md) is True:
        if Checker.eom_process_day() is False:
            eod_process()
        elif Checker.eom_process_day() is True:
            eom_process()
        print(Checker.is_weekday(md))
        print("System : Date change")
        Reporting.dbsysdate()
    else:
        print("System : Date change")
        Reporting.dbsysdate()
        Reporting.dbsysdate()


if __name__ == '__main__':
    main()

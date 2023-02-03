# This is where End  Of Day procedures are done
import datetime
import os
from typing import TextIO, Any

from src import db
from src.cob.eom import AccountsEom
from src.functions.genarators import Getters, Checker
from src.models.customer_model import Customer
from src.models.interest_model import Interest
from src.models.system_date_model import SysDate
from src.models.transaction_model import Transaction


def _write_to_file(account: Any, file: TextIO):
    for i in account:
        file.write(
            str(i.trantype) + "," + i.tranref + "," + i.tranmethod + "," + str(i.tran_date) + "," + str(
                i.cheque_num) + "," + str(i.acc_number) + "," + str(i.cr_acc_number) + "," + str(
                i.amount) + "," + str(i.custid) + "\n")


class Accounts:
    def __init__(self):
        self.account_opening = os.path.abspath(
            "../../src//reports//AccountsOpened" + Getters.getSysDate().date + ".csv")

    def accOpeningBalancing(self):
        print("Account Opening balancing")
        # Check all account opened today
        count = 0
        dt = Getters.getSysDate().date
        acc_opened = db.session.query(Transaction).filter_by(remark='Account Creation').filter_by(tran_date=dt).all()
        for i in acc_opened:
            count += float(i.amount)
        if acc_opened is not None:
            with open(self.account_opening, mode="w", encoding="utf-8") as myFile:
                _write_to_file(acc_opened, myFile)

        # update the account opening accordingly
        acc_opening_account = db.session.query(Customer).filter_by(account_type='acccreate').first()
        acc_opening_account.working_bal += count
        db.session.add(acc_opening_account)
        db.session.commit()
        # accumulate all opening balances for the new accounts
        # credit the ...acccreate.... account with the figure to zero it off
        # generate a report for all those account and the zeroing off process
        # create a list for all th entries being done

    @staticmethod
    def accountInterestEod():
        print("Account Interest")
        interest_per_annam = 0.05
        debit_interest = 0.15
        all_accounts = db.session.query(Customer).all()
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
            db.session.add(table_update)
            print("Record Account " + date + " || " + str(acc) + " || " + str(
                eod_bal) + " ==== daily interest ----" + str(interest) + " Updated on date : ----" + date)

        db.session.commit()
        print("Account interest Calculation complete")

        # check the closing balance for each account
        # calculates a daily interest for the account
        # populates the interest table with account number, interest for the day and date


class Reporting:

    def __init__(self):
        self.credit_transactions = os.path.abspath(
            "../../src//reports//CreditTransactions" + Getters.getSysDate().date + ".csv")
        self._account_closing_balances = os.path.abspath(
            "../../src/reports/AccountClosingBalances" + Getters.getSysDate().date + ".txt")

    def account_closing_balances_report(self):
        # a report of all accounts and there closing balance for the day
        acc_list = db.session.query(Customer).all()
        with open(self._account_closing_balances, mode="w", encoding="utf-8") as myfile:
            for i in acc_list:
                myfile.write(str(i.acc_number) + " : " + str(i.working_bal) + "\n")

    @staticmethod
    def teller_transaction_report():
        # report of all transactions done by each teller
        dt = Getters.getSysDate().date
        tt = Getters.getAllTts()
        with open("../../src/reports/TellerTransactions" + str(dt) + ".txt", mode="w", encoding="utf-8") as myfile:
            for i in tt:
                myfile.write(
                    str(i.id) + " : " + str(i.tran_type) + " : " + str(i.amount) + " : " + str(i.date) + " : " + str(
                        i.teller_id) + " : " + str(i.customer.acc_number) + " : " + str(i.user_id) + "\n")

    def credit_transactions_report(self):
        # all deposits done for the day
        record = db.session.query(Transaction).filter_by(tran_date=Getters.getSysDate().date).filter_by(
            trantype='CR').all()
        if record is not None:
            print("The number of records are " + str(len(record)))
            with open(self.credit_transactions, mode="w", encoding="utf-8") as myFile:
                skip_account = [acc.acc_number for acc in
                                db.session.query(Customer).filter_by(email="system@obs.com").all()]
                for i in record:
                    print("The record giving problems is" + str(i.cr_acc_number))
                    if i.cr_acc_number not in skip_account:
                        myFile.write(
                            str(i.trantype) + "," + i.tranref + "," + i.tranmethod + "," + str(i.tran_date) + "," + str(
                                i.cheque_num) + "," + str(i.acc_number) + "," + str(i.cr_acc_number) + "," + str(
                                i.amount) + "," + str(i.custid) + "\n")

    @staticmethod
    def rollover_system_date():
        date_change = db.session.query(SysDate).first()
        mydate = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        add_day = datetime.timedelta(days=1)
        new_date = mydate + add_day
        date_change.date = new_date.strftime('%Y-%m-%d')
        db.session.add(date_change)
        db.session.commit()

    @staticmethod
    def debitTransactions():
        # all withdrawals done for the day on customer account
        record = db.session.query(Transaction).filter_by(tran_date=Getters.getSysDate().date).filter_by(
            trantype='DR').all()
        with open("../../src/reports/DebitTransactions" + Getters.getSysDate().date + ".csv", mode="w",
                  encoding="utf-8") as myFile:
            _write_to_file(record, myFile)

        pass

    @staticmethod
    def accountsOpenedReport():
        # lists all the accounts opened today
        pass


def eod_process():
    print("Accounts : Accounts Opening Balancing")
    Accounts().accOpeningBalancing()
    print("Account : Account Interest End Of Day")
    Accounts.accountInterestEod()
    print("Reporting : Creadit Transaction Report")
    Reporting().credit_transactions_report()
    print("Reporting : Debit Transaction Reports")
    Reporting.debitTransactions()
    print("Reports : Account Closing Balance")
    Reporting().account_closing_balances_report()
    print("Reporting : Teller Transaction Reports")
    Reporting.teller_transaction_report()


def eom_process():
    eod_process()
    print("Updating interest to Client accounts")
    AccountsEom.accountInterestEom()
    print("Service Fee charges")
    AccountsEom.serviceFeesEom()
    Reporting().credit_transactions_report()
    print("Reporting : Debit Transaction Reports")
    Reporting.debitTransactions()
    print("Reports : Account Closing Balance")
    Reporting().account_closing_balances_report()


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
        Reporting.rollover_system_date()
    else:
        print("System : Date change")
        Reporting.rollover_system_date()
        Reporting.rollover_system_date()


if __name__ == '__main__':
    main()

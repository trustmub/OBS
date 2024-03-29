from src import db
from src.cob.log_module import SystemOBS
from src.models.customer_model import Customer
from src.models.transaction_model import Transaction


class Search:
    """This class provide methods for searchin the database."""

    # def __init__(self):
    #     self.search_logging = SystemOBS().start_logging

    _s_logging = SystemOBS.start_logging

    @classmethod
    def search_by_account(cls, account_number):
        """Search Customer record from the Customer using Account number. this is where we also log the account search
        in the logfile to ensure audit trail"""

        # self.search_logging(str(account_number))
        Search._s_logging(str(account_number))

        record = db.session.query(Customer).filter_by(acc_number=account_number).first()
        return record

    @classmethod
    def search_stmt_transactions(cls, account_number, start_date, end_date):
        """Search the Transaction table for transactions within a provided date range"""

        log_message = str(account_number) + " " + str(start_date) + " " + str(end_date)
        Search._s_logging(log_message)
        record = Search.search_by_account(account_number)

        print("Customer record object: {}".format(record))

        if record is not None:
            statement = db.session.query(Transaction).filter(Transaction.custid == record.custid).filter(
                Transaction.tran_date >= start_date).filter(Transaction.tran_date <= end_date).order_by(
                Transaction.tranid).all()
            return record, statement
        else:
            return None, []

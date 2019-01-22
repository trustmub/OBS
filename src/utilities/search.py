from src.cob.log_module import SystemOBS
from src.models import session
from src.models.models import Customer, Transactions


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

        record = session.query(Customer).filter_by(acc_number=account_number).first()
        return record

    @classmethod
    def search_stmt_transactions(self, account_number, start_date, end_date):
        """Search the Transaction table for transactions within a provided date range"""

        log_message = str(account_number) + " " + str(start_date) + " " + str(end_date)
        Search._s_logging(log_message)
        record = Search.search_by_account(account_number)

        if record is not None:
            statement = session.query(Transactions).filter(Transactions.custid == record.custid).filter(
                Transactions.tran_date >= start_date).filter(Transactions.tran_date <= end_date).order_by(
                Transactions.tranid).all()
            return record, statement
        else:
            return None, []

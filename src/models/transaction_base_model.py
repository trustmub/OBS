from dataclasses import dataclass


@dataclass
class TransactionBase(object):
    """
    main transaction class. every transaction has a date amount and credit account

    """
    def __init__(self, date, amount, cr_account):
        self.date = date
        self.amount = float(amount)
        self.cr_account = cr_account

    def __str__(self):
        return self.cr_account

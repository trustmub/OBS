from dataclasses import dataclass

from sqlalchemy import Column, Integer, String


@dataclass
class AccountType():
    """
    This table contains the type of accounts the systems handles for example, Savings current of
    Corporate Account
    """
    __tablename__ = 'account'
    id: int = Column(Integer, primary_key=True)
    acc_type: str = Column(String(10))
    minbalance: int = Column(Integer)

    def __str__(self):
        return "account type: {}".format(self.acc_type)

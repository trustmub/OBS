import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float

from src import db


@dataclass
class TransactionFeeChargeTable(db.Model):
    """
    This table contains all the transactions for charges that the clients have been charged on
    their operations including service fees. Windrawal and frasnfer charges are also captured in
    here with apropriate reference to show the type of charge.
    """
    __tablename__ = 'chargetransaction'
    id: int = Column(Integer, primary_key=True)
    tran_type: str = Column(String(10))
    dr_account: int = Column(Integer)
    cr_account: int = Column(Integer)
    charge: float = Column(Float(2))
    date: str = Column(String(30))
    create_date: str = Column(String(30), default=datetime.datetime.now())

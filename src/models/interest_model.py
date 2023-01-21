import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float

from src import db


@dataclass()
class Interest(db.Model):
    """
    This is the table where interest earnings are captured. the end of day process calculates the
    interest daily for each account and saves the values into this table for the End O Month
    precess to credit the interest earned into the respective accounts as a total figure.
    """
    __tablename__ = 'interest'
    id: int = Column(Integer, primary_key=True)
    date: str = Column(String(30))
    account: int = Column(Integer)
    eod_bal: float = Column(Float(2))
    interest_earned: float = Column(Float(2))
    create_date: str = Column(String(30), default=datetime.datetime.now())

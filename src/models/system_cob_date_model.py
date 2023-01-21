import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class CobDates(db.Model):
    """
    This table keeps a list of all the processes that have been run and marks the process with the
    system date so that if the system crashes and the EOD is reinitiated, the processes that have
    executed will not be executed again.
    """
    __tablename__ = 'cobdates'
    id: int = Column(Integer, primary_key=True)
    date: str = Column(String(30))
    process: str = Column(String(50))
    status: int = Column(Integer)
    create_date: str = Column(String(30), default=datetime.datetime.now())

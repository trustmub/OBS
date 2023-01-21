import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class Banks(db.Model):
    """
    This table contains a list of other banks which contains swift codes. This is used for external
    transfers.
    """
    __tablename__ = 'banks'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100))
    swift_code: str = Column(String(50))
    create_date: str = Column(String(30), default=datetime.datetime.now())

import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class Branch(db.Model):
    """
    This is the table for branches and their codes. Each account belongs to a particular branch the
    default branch is the head office (01) which will be created during the system setup process.
    """
    __tablename__ = 'branch'
    id: int = Column(Integer, primary_key=True)
    code: str = Column(String(5))
    description: str = Column(String(100))
    create_date: str = Column(String(30), default=datetime.datetime.now())

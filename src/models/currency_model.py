from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class Currency(db.Model):
    """
    This table contains all the currencies the system will be working using. the currencies will be
    added as the operations needs may be.
    """
    __tablename__ = 'currency'
    id: int = Column(Integer, primary_key=True)
    currency_code: str = Column(String(5))
    description: str = Column(String(100))
    create_date: str = Column(String(30))

import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class BankingServices(db.Model):
    """
    Banking services table
    """
    __tablename__ = 'banking_services'
    id: int = Column(Integer, primary_key=True)
    service_name: str = Column(String(50))
    service_description: str = Column(String(200))
    created_date: str = Column(String(30), default=datetime.datetime.now())

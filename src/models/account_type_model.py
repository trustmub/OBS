from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import registry

from src import db

mapper_registry = registry()


@dataclass
class AccountType(db.Model):
    """
    This table contains the type of accounts the systems handles for example, Savings current of
    Corporate Account
    """
    __tablename__ = 'account_type'
    id: int = Column(Integer, primary_key=True)
    acc_type: str = Column(String(10))
    minbalance: int = Column(Integer)

    def __str__(self):
        return "account type: {}".format(self.acc_type)

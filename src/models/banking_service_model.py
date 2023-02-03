from __future__ import annotations

import datetime
from dataclasses import dataclass

from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import registry

from src import db

mapper_register = registry()


# @mapper_register.mapped
@dataclass
class BankServices(db.Model):
    """
    This table contains a list of other banks which contains swift codes. This is used for external
    transfers.
    """
    # db.__table__ = Table(
    #     "banking_services",
    #     mapper_register.metadata,
    #     db.Column("id", Integer, primary_key=True),
    #     db.Column("service_name", String(50)),
    #     db.Column("service_description", String(200)),
    #     db.Column("created_date", String(30), default=datetime.datetime.now())
    # )
    #
    # id: int = field(init=False)
    # service_name: str = Optional[str]
    # service_description: str = Optional[str]
    # created_date: str = Optional[str]

    __tablename__ = 'bankingservices'
    id: int = Column(Integer, primary_key=True)
    service_name: str = Column(String(50))
    service_description: str = Column(String(200))
    created_date: str = Column(String(30), default=datetime.datetime.now())

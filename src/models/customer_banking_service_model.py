import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from src import db
from src.models.banking_service_model import BankServices


@dataclass
class CustomerBankingService(db.Model):
    __tablename__ = "registered_services"
    id: int = Column(Integer, primary_key=True)
    # api_user_id: int = Column(Integer, ForeignKey('api_user.user_id'))
    # api_user = relationship(ApiUser)
    service_id: int = Column(Integer, ForeignKey('banking_services.id'))
    service: int = relationship(BankServices)
    status: str = Column(String(10))
    created_date: str = Column(String(30), default=datetime.datetime.now())

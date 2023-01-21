import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src import db
from src.models.system_user_model import SystemUser


@dataclass
class Till(db.Model):
    """
    This table keeps the teller accounts and each teller account is linked to a user_view ID which
    helps to identify the user_view who is linked to the teller account for tracking transactions
    flow.
    """
    __tablename__ = 'till'
    id: int = Column(Integer, primary_key=True)
    branch_code: str = Column(String(10))
    o_balance: float = Column(Float(2))
    c_balance: float = Column(Float(2))
    till_account: str = Column(String(15))
    currency: str = Column(String())
    remark: str = Column(String(100))
    date: str = Column(String(30))
    create_date: str = Column(String(30), default=datetime.datetime.now())

    user_id: int = Column(Integer, ForeignKey('user.uid'), nullable=True)
    user = relationship(SystemUser)


# class TillSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'branch_code', 'till_account', 'currency', 'remark')
#
#
# till_schema = TillSchema()
# tills_schema = TillSchema(many=True)

# @dataclass
# class BankingServices(db.Model):
#     __tablename__ = 'bankingservices'
#     id: int = Column(Integer, primary_key=True)
#     service_name: str = Column(String(50))
#     service_description: str = Column(String(200))
#     created_date: str = Column(String(30), default=datetime.datetime.now())

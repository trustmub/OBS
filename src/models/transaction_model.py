from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src import db
from src.models.customer_model import Customer


@dataclass
class Transaction(db.Model):
    """
    This table contains all the client transaction that are done in the system. these include
    Withdrawal, Deposits, transfers that affect the client account.
    """
    __tablename__ = 'transactions'
    tranid: int = Column(Integer, primary_key=True)
    trantype: str = Column(String(10))
    tranref: str = Column(String(15))
    tranmethod: str = Column(String(50))
    tran_date: str = Column(String(30))
    cheque_num: str = Column(String(30))
    acc_number: int = Column(Integer)
    cr_acc_number: int = Column(Integer)
    amount: float = Column(Float(2))
    current_balance: float = Column(Float(2))
    remark: str = Column(String(200))

    custid = Column(Integer, ForeignKey('customer.custid'))
    customer = relationship(Customer)

    create_date = Column(String(30))

# class TransactionSchema(ma.Schema):
#     class Meta:
#         fields = ('tranid', 'trantype', 'tranref', 'tranmethod', 'acc_number')
#
#
# transaction_schema = TransactionSchema()
# transactions_schema = TransactionSchema(many=True)

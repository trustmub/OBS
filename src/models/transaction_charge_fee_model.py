from dataclasses import dataclass

from sqlalchemy import Column, Integer, Float, String

from src import db


@dataclass
class TransactionChargeFee(db.Model):
    """
    This table keeps the charge fees for each respective Transaction type. additional transaction
    typex can be added in the transaction type table
    """
    __tablename__ = 'transactioncharge'
    id: int = Column(Integer, primary_key=True)
    tran_type: str = Column(String(10))
    tran_charge: float = Column(Float(2))
    create_date: str = Column(String(30))

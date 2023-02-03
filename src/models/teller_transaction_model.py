from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src import db
from src.models.customer_model import Customer
from src.models.system_user_model import SystemUser
from src.models.till_model import Till


@dataclass
class TellerTransaction(db.Model):
    """
    This table contains all the transactions a teller does. Each transaction a teller does i
    linked to their teller ID and the Till Account ID. The transaction is also linked to the client
    Account ID enabling a complete trail of the transaction flow.
    """
    __tablename__ = 'tellertransactions'
    id: int = Column(Integer, primary_key=True)
    tran_type: str = Column(String(10))
    tranref: str = Column(String(15))
    amount: float = Column(Float(2))
    date: str = Column(String(30))
    remark: str = Column(String(100))
    create_date: str = Column(String(30))

    teller_id = Column(Integer, ForeignKey('till.id'))
    teller = relationship(Till)

    customer_id = Column(Integer, ForeignKey('customer.custid'))
    customer = relationship(Customer)

    user_id = Column(Integer, ForeignKey('user.uid'))
    user = relationship(SystemUser)

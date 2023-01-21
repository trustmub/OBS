import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src import db
from src.models.card_model import Card
from src.models.system_user_model import SystemUser


@dataclass
class Customer(db.Model):
    """
    THis table contains all the customer details.
    """
    __tablename__ = 'customer'
    custid: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(100))
    last_name: str = Column(String(100))
    dob: str = Column(String(15))
    address: str = Column(String(256))
    country: str = Column(String(100))
    email: str = Column(String(100))
    gender: str = Column(String(30))
    contact_number: str = Column(String(20))
    working_bal: float = Column(Float(2))
    acc_number: int = Column(Integer)
    account_type: str = Column(String(10))
    create_date: str = Column(String(30), default=datetime.datetime.now())
    # services = Column(postgresql.ARRAY(Integer, dimensions=1))
    # signature_img = Column(String(100))

    card_id = Column(Integer, ForeignKey("card.id"))
    card = relationship(Card)
    #
    inputter_id: int = Column(Integer, ForeignKey('user.uid'))
    inputter = relationship(SystemUser)

    @property
    def full_name(self):
        """
        full name as a property
        :return: first_name and last_name
        """
        return "{} {}".format(self.first_name, self.last_name)

# class CustomerSchema(ma.Schema):
#     class Meta:
#         fields = ('custid', 'first_name', 'last_name')
#
#
# customer_schema = CustomerSchema()
# customers_schema = CustomerSchema(many=True)

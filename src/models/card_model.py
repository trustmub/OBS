# import datetime
# from dataclasses import dataclass
#
# from sqlalchemy import Column, Integer, String
#
# from src import db
import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class Card(db.Model):
    __tablename__ = "card"
    id: int = Column(Integer, primary_key=True)
    card_number: int = Column(String(15))
    account_number: int = Column(Integer)
    card_type: str = Column(String(100))
    created_date: str = Column(String(30), default=datetime.datetime.now())


# class CardSchema:
#     class Meta:
#         fields = ('id', 'card_number', 'account_number', 'card_type', 'create_cate')
#
#
# card_schema = CardSchema()

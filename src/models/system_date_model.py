import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class SysDate(db.Model):
    """
    This table keeps the current system date since the last End Of Day (EOD) process. When the end
    of day completes the date is changes to the next trading date.
    """
    __tablename__ = 'sysdate'
    id: int = Column(Integer, primary_key=True)
    date: str = Column(String(30))
    create_date: str = Column(String(30), default=datetime.datetime.now())

# class SysDateSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'date', 'create_date')
#
#
# sys_date_schema = SysDateSchema()

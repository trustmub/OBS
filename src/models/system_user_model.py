from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Float

from src import db


@dataclass
class SystemUser(db.Model):
    """
    This table contains all the systems users from the teller, backend operations and system users.
    """
    __tablename__ = 'user'
    uid: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(100))
    job_title: str = Column(String(100))
    image_string: str = Column(String(100))
    department: str = Column(String(50))
    branch_code: str = Column(String(15))
    access_level: int = Column(Integer)
    till_o_balance: float = Column(Float(2))
    till_c_balance: float = Column(Float(2))
    create_date: str = Column(String(30))
    email: str = Column(String(60))
    password: str = Column(String(100))
    lock: int = Column(Integer)

# class SystemUserSchema(ma.Schema):
#     class Meta:
#         fields = ('uid',
#                   'full_name',
#                   'job_title',
#                   'department',
#                   'branch_code',
#                   'access_level',
#                   'till_o_balance',
#                   'till_c_balance',
#                   'create_date',
#                   'email')
#
#
# system_user_schema = SystemUserSchema()
# system_users_schema = SystemUserSchema(many=True)

import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserHistory(Base):
    """This table contains all the systems users from the teller, backend operations and system users"""
    __tablename__ = 'user_history'
    uid = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    job_title = Column(String(100))
    image_string = Column(String(100))
    department = Column(String(50))
    branch_code = Column(String(15))
    access_level = Column(Integer)
    till_o_balance = Column(Float(2))
    till_c_balance = Column(Float(2))
    create_date = Column(String(30))
    email = Column(String(60))
    password = Column(String(100))
    lock = Column(Integer)

    def __init__(self, full_name, job_title, image_string, department, branch_code, access_level, till_o_balance,
                 till_c_balance, email, password, lock):
        self.full_name = full_name
        self.job_title = job_title
        self.image_string = image_string
        self.department = department
        self.branch_code = branch_code
        self.access_level = access_level
        self.till_o_balance = till_o_balance
        self.till_c_balance = till_c_balance
        self.create_date = datetime.datetime.now()
        self.email = email
        self.password = password
        self.lock = lock


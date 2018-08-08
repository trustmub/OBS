"""
    controller.user
    ---------------

    A user controller that provide functionalities for the user resgistration login and ammendments of user record.

    this controller interacts with the user views.user module
"""

from models.db_conn import session
from models.models import User
from flask_bcrypt import Bcrypt


class UserBase(object):
    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.password = password


class UserController(object):
    def __init__(self,
                 full_name,
                 email,
                 password,
                 job_title='',
                 image_string='',
                 department='',
                 branch_code='',
                 access_level=0,
                 till_o_balance=0,
                 till_c_balance=0,
                 lock=0):
        self.job_title = job_title
        self.image_string = image_string
        self.department = department
        self.branch_code = branch_code
        self.access_level = access_level
        self.till_o_balance = till_o_balance
        self.till_c_balance = till_c_balance
        self.lock = lock
        self.full_name = full_name
        self.email = email
        self.password = password

    def add_new_user(self):
        new_record = User(full_name=self.full_name,
                          job_title=self.job_title,
                          image_string=self.image_string,
                          department=self.department,
                          branch_code=self.branch_code,
                          access_level=self.access_level,
                          till_o_balance=self.till_o_balance,
                          till_c_balance=self.till_c_balance,
                          email=self.email,
                          password=self.encrypted_password,
                          lock=self.lock
                          )
        session.add(new_record)
        session.commit()

    @property
    def encrypted_password(self):
        bcrypt = Bcrypt()
        pwd = bcrypt.generate_password_hash(self.password, 12)
        return pwd

    def email_exists(self):
        if session.query(User).filter_by(email=self.email).first(): return True

    def update_user(self):
        old_user = session.query(User).filter_by(email=self.email).first()

        if old_user.full_name != self.full_name or '': old_user.full_name = self.full_name
        if old_user.job_title != self.job_title or '': old_user.job_title = self.job_title
        if old_user.image_string != self.image_string or '': old_user.image_string = self.image_string
        if old_user.department != self.department or '': old_user.department = self.department
        if old_user.branch_code != self.branch_code or '': old_user.branch_code = self.branch_code
        if old_user.access_level != self.access_level or 0: old_user.access_level = self.access_level
        if old_user.till_o_balance != self.till_o_balance or 0: old_user.till_o_balance = self.till_o_balance
        if old_user.till_c_balance != self.till_c_balance or 0: old_user.till_c_balance = self.till_c_balance

        session.add(old_user)
        session.commit()
        return

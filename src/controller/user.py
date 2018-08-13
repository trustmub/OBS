"""
    controller.user
    ---------------

    A user controller that provide functionalities for the user resgistration login and amendments
    of user record.

    this controller interacts with the user views.user module
"""

from flask_bcrypt import Bcrypt
from src.models.models import User
from src.controller import session


class UserController(object):
    """
    Handles all the functions for persisting to database whci are Create, Update and
    Delete
    """

    def __init__(self,
                 email,
                 password,
                 full_name='',
                 job_title='',
                 image_string='avatar.png',
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
        """
        Method to add new user record
        :return: None
        """
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
                          lock=self.lock)
        session.add(new_record)
        session.commit()

    @property
    def encrypted_password(self):
        """
        Property Method to encrypt the passed password.
        :return: byte string
        """
        bcrypt = Bcrypt()
        password = bcrypt.generate_password_hash(self.password, 12)
        return password

    def verify_email(self):
        """
        Method to check is email exists
        :return: Boolean
        """
        if session.query(User).filter_by(email=self.email).first():
            return True

    def verify_password(self):
        """
        Method to verify password
        :return: Boolean
        """
        user = session.query(User).filter_by(email=self.email).first()
        if Bcrypt().check_password_hash(user.password, self.password):
            return True

    def update_user(self):
        """
        Method to update the user profile.
        :return: None
        """
        old_user = session.query(User).filter_by(email=self.email).first()

        if old_user.full_name != self.full_name or '':
            old_user.full_name = self.full_name
        if old_user.job_title != self.job_title or '':
            old_user.job_title = self.job_title
        if old_user.image_string != self.image_string or '':
            old_user.image_string = self.image_string
        if old_user.department != self.department or '':
            old_user.department = self.department
        if old_user.branch_code != self.branch_code or '':
            old_user.branch_code = self.branch_code
        if old_user.access_level != self.access_level or 0:
            old_user.access_level = self.access_level
        if old_user.till_o_balance != self.till_o_balance or 0:
            old_user.till_o_balance = self.till_o_balance
        if old_user.till_c_balance != self.till_c_balance or 0:
            old_user.till_c_balance = self.till_c_balance

        session.add(old_user)
        session.commit()

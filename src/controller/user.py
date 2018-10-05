"""
    controller.user
    ---------------

    A user controller that provide functionalities for the user resgistration login and amendments
    of user record.

    this controller interacts with the user views.user module
"""

from src import bcrypt
from src.models.models import User
from . import session


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
                 access_level=1,
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
        Method to add new user record into the database
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
        Property Method to encrypt self.password.
        :return:
            encrypted string of self.password by 12 cycles/rounds.
        """
        password = bcrypt.generate_password_hash(self.password, 12)
        return password

    def verify_email(self):
        """
        Method to check if email exists
        :return:
            True id self.email exists and None/False if self.email does not exist.
        """
        if session.query(User).filter_by(email=self.email).first():
            return True

    def verify_password(self):
        """
        Method to verify password
        :return:

            True if self.password correct and None/False if self.password is wrong
        """
        user = session.query(User).filter_by(email=self.email).first()
        if bcrypt.check_password_hash(user.password, self.password):
            return True

    def update_user(self):
        """
        Method to update the user profile.

        requisite fields:

            - full_name
            - job_title
            - department
            - branch_code
            - access_level
            - image_string
        """

        user = session.query(User).filter_by(email=self.email).first()

        user.full_name = self.full_name
        user.job_title = self.job_title
        user.department = self.department
        user.branch_code = self.branch_code
        user.access_level = self.access_level
        if self.image_string != '':
            user.image_string = self.image_string

        session.add(user)
        session.commit()

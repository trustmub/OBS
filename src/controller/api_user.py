from src import bcrypt
from src.models.models import Customer, ApiUser
from . import session


class ApiUserController(object):
    def __init__(self, account, pin, user_number=1, device="default"):
        self.account = account
        self.pin = pin
        self.device = device
        self.user_number = user_number

    def check_account_exists(self):
        if session.query(Customer).filter_by(acc_number=self.account).first():
            return True
        return False

    def customer_details(self) -> object:
        customer = session.query(Customer).filter_by(acc_number=self.account).first()
        return customer.serialize

    def user_details(self) -> object:
        """
        This method will return the ApiUser Object serialised according to the serialize property

        :return:

            JSON object of ApiUser detail
        """
        details = session.query(ApiUser).filter_by(account_number=self.account).first()
        return details.serialize

    def create_mobile_account(self):
        new_mobile_user = ApiUser(account_number=int(self.account),
                                  pin=self.pin,
                                  device=self.encrypted_pin,
                                  user_number=self.user_number)

        session.add(new_mobile_user)
        session.commit()

    @property
    def encrypted_pin(self):
        """
        Property Method to encrypt self.pin. the pin will be converted to string first. this is because
        integer values are not iterable
        :return:
            encrypted string of self.password by 12 cycles/rounds. 12 rounds is the default value which can be omitted
            on the parameters
        """
        pin = bcrypt.generate_password_hash(self.device)
        return pin

    def verify_account(self):
        """
        Method to check if account number exists in the Customer table
        :return:
            True id self.email exists and None/False if self.email does not exist.
        """
        if session.query(Customer).filter_by(acc_number=self.account).first():
            return True
        return False

    def verify_pin(self):
        """
        Method to verify pin
        :return:

            True if self.pin correct and None/False if self.pin is wrong
        """
        user = session.query(ApiUser).filter_by(account_number=self.account).first()

        if user and bcrypt.check_password_hash(user.device, self.device):
            return True

    def verify_registration(self):
        """
        this methods verifies the existence (or non-existence) of the account in the customer table

        :return:

            True if record exists
        """
        if session.query(ApiUser).filter_by(account_number=self.account).first():
            return True

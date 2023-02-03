from sqlalchemy.exc import ArgumentError

from src import db
from src.models.api_user_model import ApiUser
from src.models.banking_service_model import BankServices
from src.models.customer_banking_service_model import CustomerBankingService


class BankingServicesController(object):

    def __init__(self, account_number):
        self.account_number = int(account_number)

    @staticmethod
    def add_banking_service(service_name, description):
        service = BankServices(service_name=service_name, service_description=description)
        db.session.add(service)
        db.session.commit()

    def link_banking_service(self, service_id):
        api_user = db.session.query(ApiUser).filter_by(account_number=self.account_number).first()
        service = db.session.query(BankServices).filter_by(id=int(service_id))

        record = CustomerBankingService(api_user_id=api_user.user_id,
                                        service_id=service_id,
                                        status="active")
        db.session.add(record)
        db.session.commit()

    def customer_banking_services(self) -> list:
        try:
            api_user_id = db.session.query(ApiUser).filter_by(account_number=self.account_number).first()
            if api_user_id is not None:
                service_list = db.session.query(CustomerBankingService).filter_by(api_user_id=api_user_id.user_id).all()
                return [service.serialize for service in service_list]
            return []
        except ArgumentError as e:
            print(e)
            return []

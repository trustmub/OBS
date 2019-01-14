from sqlalchemy.exc import ArgumentError

from src.models import session
from src.models.models import BankingServices, ApiUser, CustomerBankingService


class BankingServicesController(object):

    def __init__(self, account_number):
        self.account_number = int(account_number)

    @staticmethod
    def add_banking_service(service_name, description):
        service = BankingServices(service_name=service_name, service_description=description)
        session.add(service)
        session.commit()

    def link_banking_service(self, service_id):
        api_user = session.query(ApiUser).filter_by(account_number=self.account_number).first()
        service = session.query(BankingServices).filter_by(id=int(service_id))

        record = CustomerBankingService(api_user_id=api_user.user_id,
                                        service_id=service_id,
                                        status="active")
        session.add(record)
        session.commit()

    def customer_banking_services(self) -> list:
        try:
            api_user_id = session.query(ApiUser).filter_by(account_number=self.account_number).first()
            if api_user_id is not None:
                service_list = session.query(CustomerBankingService).filter_by(api_user_id=api_user_id.user_id).all()
                return [service.serialize for service in service_list]
            return []
        except ArgumentError as e:
            print(e)
            return []

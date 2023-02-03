from flask import Blueprint

from src.models.banking_service_model import BankServices
from src.models.interest_model import Interest
from src.models.system_cob_date_model import CobDates

eod_view = Blueprint('eod_view', __name__)


def _placeholder_function():
    bank_service = BankServices()
    interest = Interest()
    cob_dates = CobDates()

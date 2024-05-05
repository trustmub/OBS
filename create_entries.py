import datetime
import string
import time
import random

from src import db
from src.models.card_model import Card
from src.models.system_user_model import SystemUser
from src.utils.genarators import Auto
from src.models.account_type_model import AccountType
from src.models.banking_service_model import BankServices
from src.models.branch_model import Branch
from src.models.currency_model import Currency
from src.models.customer_model import Customer
from src.models.system_date_model import SysDate
from src.models.till_model import Till
from src.models.transaction_charge_fee_model import TransactionChargeFee


def create_system_date():
    date_obj = db.session.query(SysDate).all()
    if not date_obj:
        sys_date = SysDate(date=time.strftime('%Y-%m-%d'))
        db.session.add(sys_date)
        db.session.commit()
    else:
        print("System Date Already Set To: {}".format(date_obj[0].date))


def create_system_user():
    user = SystemUser(
        full_name="System User",
        job_title="System User",
        department="System User",
        branch_code="Default",
        email="systemuser@obs.com",
        password="systemuser",
        access_level=0,
        lock=1,
    )

    db.session.add(user)
    db.session.commit()

    return user.uid


system_user_id = create_system_user()


def create_system_card(accountNo):
    card_no = random.choices(string.digits, k=15)
    print("card number generated: {}".format(''.join(card_no)))
    card = Card(
        card_number=str(''.join(card_no)),
        account_number=accountNo,
        card_type="Default"
    )
    db.session.add(card)
    db.session.commit()
    return card.id


def create_system_accounts():
    account_types = ["rtgs", "charges", "suspense", "servfee", "acccreate", "interest"]
    contact_number_counter = 772000000

    existing_account_types = {at.account_type for at in Customer.query.all()}

    for account_type in account_types:
        account_number = Auto().account_number_generator()
        card_id = create_system_card(account_number)

        if account_type not in existing_account_types:
            print(f"Creating account of type {account_type}.")
            contact_number = str(contact_number_counter).zfill(10)
            record = Customer(
                first_name='sys_user',
                last_name='sys_user',
                dob=time.strftime('%Y-%m-%d'),
                address='Head Office',
                country='Zimbabwe',
                email='system@obs.com',
                gender='system',
                contact_number=contact_number,
                working_bal=0,
                acc_number=account_number,
                account_type=account_type,
                inputter_id=system_user_id,
                card_id=card_id,

            )
            db.session.add(record)
            db.session.commit()
            contact_number_counter += 1


def create_system_tellers():
    record_till = db.session.query(Till).all()
    if len(record_till) <= 6:
        for _ in range(0, 6):
            print("Teller account created")
            new_teller = Till(
                branch_code='',
                o_balance=0,
                c_balance=0,
                till_account=Auto().system_account_number_generator(),
                currency="USD",
                remark='',
                date='',
                user_id=system_user_id)
            db.session.add(new_teller)
            db.session.commit()


def create_system_currencies():
    currencies = [{"currency_code": "USD", "description": "United States Dollar"},
                  {"currency_code": "ZAR", "description": "South African Rand"},
                  {"currency_code": "GBP", "description": "Great Britain Pound"}]

    for currency in currencies:
        code = currency.get("currency_code")
        description = currency.get("description")
        if code not in [c.currency_code for c in db.session.query(Currency).all()]:
            new_currency = Currency(currency_code=code, description=description,
                                    create_date=str(datetime.datetime.now()))
            db.session.add(new_currency)
        else:
            continue
        print("System currencies created")
        db.session.commit()


def create_system_branches():
    branches = [{"code": "01", "description": "Head Office"},
                {"code": "02", "description": "Treasury"},
                {"code": "03", "description": "Reconciliation"}]
    for branch in branches:
        branch_code = branch.get("code")
        description = branch.get("description")
        if branch_code not in [b.code for b in db.session.query(Branch).all()]:
            new_branch = Branch(code=branch_code, description=description)
            db.session.add(new_branch)
            db.session.commit()
        else:
            continue


def create_transaction_charge_type():
    charge_types = [{"tran_type": "CR", "tran_charge": 0},
                    {"tran_type": "DR", "tran_charge": 1.50},
                    {"tran_type": "TR", "tran_charge": 1.0},
                    {"tran_type": "RTGS", "tran_charge": 5.0},
                    {"tran_type": "SF", "tran_charge": 3.0}]

    for charge in charge_types:
        trans_type = charge.get("tran_type")
        trans_charge = charge.get("tran_charge")
        if trans_type not in [chg.tran_type for chg in db.session.query(TransactionChargeFee).all()]:
            new_charge = TransactionChargeFee(tran_type=trans_type, tran_charge=trans_charge)
            db.session.add(new_charge)
            db.session.commit()
            print("Charge Type created")
        else:
            continue


def create_account_type():
    account_types = [{"acc_type": "Savings", "minbalance": 0},
                     {"acc_type": "Current", "minbalance": 5},
                     {"acc_type": "Corporate", "minbalance": 100}]
    for account_type in account_types:
        type_name = account_type.get("acc_type")
        min_balance = account_type.get("minbalance")
        if type_name not in [t.acc_type for t in db.session.query(AccountType).filter_by(acc_type=type_name).all()]:
            new_type = AccountType(acc_type=type_name, minbalance=min_balance)
            print("Account types created")
            db.session.add(new_type)
            db.session.commit()
        else:
            continue


def create_banking_services():
    service_dictionary = [{"service_name": "Pay", "service_description": "for payments"},
                          {"service_name": "Transfer", "service_description": "Transfer funds to local banks"},
                          {"service_name": "CashSend", "service_description": "E-wallet services"},
                          {"service_name": "Bill Payments", "service_description": "Bill Payments"}]
    for service in service_dictionary:

        service_n = service.get("service_name")
        service_d = service.get("service_description")

        existing_services = db.session.query(BankServices).filter_by(service_name=service_n).all()

        if service_n not in [s.service_name for s in existing_services]:
            service_record: BankServices = BankServices(service_name=service_n, service_description=service_d)
            print("Banking service: {} create".format(service_n))
            db.session.add(service_record)
        else:
            continue
        db.session.commit()


def create_application_defaults():
    create_system_date()
    create_system_accounts()
    create_system_currencies()
    create_system_tellers()
    create_system_branches()
    create_transaction_charge_type()
    create_banking_services()
    create_account_type()


if __name__ == '__main__':
    create_application_defaults()

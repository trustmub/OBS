import time
import datetime
from src.models import session
from src.models.models import SysDate, Till, TransactionCharge, Account, Branch, Currency, Customer, BankingServices
from src.functions.genarators import Auto


def create_system_date():
    date_obj = session.query(SysDate).all()
    if not date_obj:
        sys_date = SysDate(date=time.strftime('%Y-%m-%d'), create_date=datetime.datetime.now())
        session.add(sys_date)
        session.commit()
    else:
        print("System Date Already Set To: {}".format(date_obj[0].date))


def create_system_accounts():
    account_types = [{"type": "rtgs"},
                     {"type": "charges"},
                     {"type": "suspense"},
                     {"type": "servfee"},
                     {"type": "acccreate"},
                     {"type": "interest"}
                     ]
    contact_number_counter = 772000000
    for acc_type in account_types:
        account_type = acc_type.get("type")
        if account_type not in [at.account_type for at in session.query(Customer).all()]:
            print("Account of type {} create.".format(account_type))
            contact_number = str(contact_number_counter).zfill(10)
            record = Customer(first_name='sys_user', last_name='sys_user', dob=time.strftime('%Y-%m-%d'),
                              address='Head Office', country='Zimbabwe', email='system@obs.com', gender='system',
                              contact_number=contact_number, working_bal=0,
                              acc_number=Auto().account_number_generator(),
                              account_type=account_type, create_date=datetime.datetime.now(), inputter_id=1)
            session.add(record)
            session.commit()
            contact_number_counter += 1
        else:
            continue


def create_system_tellers():
    record_till = session.query(Till).all()
    if len(record_till) <= 6:
        for _ in range(0, 6):
            print("Teller account created")
            new_teller = Till(branch_code='', o_balance=0, c_balance=0,
                              till_account=Auto().system_account_number_generator(),
                              currency="USD", remark='', date='', create_date=datetime.datetime.now(), user_id='')
            session.add(new_teller)
            session.commit()


def create_system_currencies():
    currencies = [{"currency_code": "USD", "description": "United States Dollar"},
                  {"currency_code": "ZAR", "description": "South African Rand"},
                  {"currency_code": "GBP", "description": "Great Britain Pound"}]

    for currency in currencies:
        code = currency.get("currency_code")
        description = currency.get("description")
        if code not in [c.currency_code for c in session.query(Currency).all()]:
            new_currency = Currency(currency_code=code, description=description, create_date=datetime.datetime.now())
            session.add(new_currency)
            session.commit()
        else:
            continue


def create_system_branches():
    branches = [{"code": "01", "description": "Head Office"},
                {"code": "02", "description": "Treasury"},
                {"code": "03", "description": "Reconciliation"}]
    for branch in branches:
        branch_code = branch.get("code")
        description = branch.get("description")
        if branch_code not in [b.code for b in session.query(Branch).all()]:
            new_branch = Branch(code=branch_code, description=description)
            session.add(new_branch)
            session.commit()
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
        if trans_type not in [chg.tran_type for chg in session.query(TransactionCharge).all()]:
            new_charge = TransactionCharge(tran_type=trans_type, tran_charge=trans_charge)
            session.add(new_charge)
            session.commit()
            print("Charge Type created")
        else:
            continue


def create_account_type():
    account_types = [{"acc_type": "Savings", "minbalance": 0},
                     {"acc_type": "Current", "minbalance": 5},
                     {"acc_type": "Corporate", "minbalance": 100}]
    for type in account_types:
        type_name = type.get("acc_type")
        min_balance = type.get("minbalance")
        if type_name not in [t.acc_type for t in session.query(Account).filter_by(acc_type=type_name).all()]:
            new_type = Account(acc_type=type_name, minbalance=min_balance)
            print("Account types created")
            session.add(new_type)
            session.commit()
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

        if service_n not in [s.service_name for s in
                             session.query(BankingServices).filter_by(service_name=service_n).all()]:
            service_record = BankingServices(service_name=service_n, service_description=service_d)
            print("Banking service: {} create".format(service_n))
            session.add(service_record)
            session.commit()
        else:
            continue


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

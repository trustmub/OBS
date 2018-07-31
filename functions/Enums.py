from aenum import Enum


class TransactionType(Enum):
    CREDIT = 'CR'
    DEBIT = 'DR'
    SERVICE_FEE = 'SF'
    RTGS = 'RTGS'
    TRANSFER = 'TR'
    CR_DR = 'CR DR'


class TransactionCategory(Enum):
    pass


class TransactionMethod(Enum):
    CASH = 'Cash'
    TRANSFER = 'TR'

class AccountTypes(Enum):
    CHARGES = 'charges'
    SERVICE_FEES = 'servfee'
    ACCOUNT_CREATION = 'acccreate'

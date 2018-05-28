from aenum import Enum


class TransactionType(Enum):
    CREDIT = 'CR'
    DEBIT = 'DR'
    SERVICE_FEE = 'SF'
    RTGS = 'RTGS'
    TRANSFER = 'TR'


class TransactionCategory(Enum):
    pass


class TransactionMethod(Enum):
    CASH = 'Cash'
    TRANSFER = 'TR'

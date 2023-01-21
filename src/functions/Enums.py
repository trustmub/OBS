from aenum import Enum


class TransactionType(Enum):
    CREDIT = 'CR'
    DEBIT = 'DR'
    SERVICE_FEE = 'SF'
    RTGS = 'RTGS'
    TRANSFER = 'TR'
    CR_DR = 'CR DR'

    def __str__(self):
        return self.string


class TransactionCategory(Enum):
    pass


class TransactionMethod(Enum):
    CASH = 'Cash'
    TRANSFER = 'TR'

    def __str__(self):
        return self.string


class AccountTypes(Enum):
    CHARGES = 'charges'
    SERVICE_FEES = 'servfee'
    ACCOUNT_CREATION = 'acccreate'

    def __str__(self):
        return self.value

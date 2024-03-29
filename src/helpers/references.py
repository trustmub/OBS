import datetime
import random

from src.utils.genarators import Getters
from .. import db
from ..models.transaction_model import Transaction

_alphabet = ['a', 'b', 'c', 'd', 'e', 'f',
             'g', 'h', 'i', 'j', 'k', 'l',
             'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x',
             'y', 'z']



class References:

    def __init__(self):
        self._transaction_references = [i.tranref for i in db.session.query(Transaction).all()]
        self._reference = self._generate_transaction_reference

    @property
    def _generate_transaction_reference(self):
        sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
        time_component = sys_date.strftime("%y%m%d")
        random.shuffle(_alphabet)
        rand_string = random.sample(_alphabet, 5)
        alp = "".join(rand_string)
        ref_str = "FT" + str(time_component) + alp.upper()
        return ref_str

    @property
    def get_transaction_reference(self):
        while True:
            self._reference = self._generate_transaction_reference
            if self._reference in self._transaction_references:
                continue
            else:
                return self._reference

        # if is_transaction_reference_available(reference):
        #     get_transaction_reference()
        # return reference


def generate_transaction_reference():
    # sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
    time_component = sys_date.strftime("%Y%m%d")
    random.shuffle(_alphabet)
    rand_string = random.sample(_alphabet, 5)
    alp = "".join(rand_string)
    ref_str = "FT" + str(time_component) + alp.upper()
    return ref_str


def is_transaction_reference_available(transaction_reference):
    transaction_list = [i.tranref for i in db.session.query(Transaction).all()]
    if transaction_reference in transaction_list:
        return False
    return True


def get_transaction_reference():
    while True:
        reference = generate_transaction_reference()
        if not is_transaction_reference_available(reference):
            continue
        else:
            return reference

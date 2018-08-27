import datetime
import random
from src.functions.genarators import Getters
from . import session

def generate_transaction_reference():
    return 'wewew'


def get_transaction_reference():
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')
    time_component = sys_date.strftime("%y%m%d")
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    random.shuffle(alphabet)
    rand_string = random.sample(alphabet, 5)
    alp = "".join(rand_string)
    ref_str = "FT" + str(time_component) + alp.upper()

    transaction_list = [i.tranref for i in session.query(Transactions).all()]

    if ref_str in transaction_list:
        reference_string_generator()
    else:
        return ref_str

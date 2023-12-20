import functools
import warnings

from src import db
from src.models.bank_table_model import Banks
from src.models.branch_model import Branch
from src.models.currency_model import Currency
from src.models.system_date_model import SysDate


class SystemUtil:


    @staticmethod
    def get_registered_banks():
        return db.session.query(Banks).all()

    @staticmethod
    def get_system_branches():
        return db.session.query(Branch).all()

    @staticmethod
    def get_system_currencies():
        return db.session.query(Currency).all()

    @staticmethod
    def get_system_date():
        return db.session.query(SysDate).first()





def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


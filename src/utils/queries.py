from src import db
from src.utils.user_profile import Profile
from src.models.till_model import Till
from src.models.transaction_charge_fee_model import TransactionChargeFee


class Query:
    def __init__(self):
        self.transaction_type = db.session.query(TransactionChargeFee).all()
        self._available_teller_accounts = db.session.execute(db.select(Till).filter_by(user_id=0)).scalars()
        self.teller_list = db.session.query(Till).all()

    def transaction_types(self):
        return self.transaction_type

    def available_tellers(self):
        return self._available_teller_accounts

    def all_tellers(self):
        return self.teller_list

    def teller_status(self):
        mylist = [i.user_id for i in self.teller_list]
        if Profile().user_details().uid in mylist:
            return True

    def till_details(self):
        _teller_id_list = [i.id for i in self.teller_list]
        _profile_id = Profile().user_details().uid
        if _profile_id in _teller_id_list:
            return db.session.query(Till).filter_by(user_id=_profile_id).first()
        else:
            return []

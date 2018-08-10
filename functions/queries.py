from functions.genarators import Profile
from models import session
from models.models import TransactionCharge, Till


class Query:
    def __init__(self):
        self.transaction_type = session.query(TransactionCharge).all()
        self._available_teller_accounts = session.query(Till).filter_by(user_id='').all()
        self.teller_list = session.query(Till).all()

    def transaction_types(self):
        return self.transaction_type

    def available_tellers(self):
        return self._available_teller_accounts

    def all_tellers(self):
        return self.teller_list

    def teller_status(self):
        mylist = [i.user_id for i in self.teller_list]
        if Profile().user_details().uid in mylist:
            return 1

    def till_details(self):
        _teller_id_list = [i.id for i in self.teller_list]
        _profile_id = Profile().user_details().uid
        if _profile_id in _teller_id_list:
            return session.query(Till).filter_by(user_id=_profile_id).first()
        else:
            return []

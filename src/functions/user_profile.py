from dataclasses import dataclass

from flask import session

from src import db
from src.models.system_user_model import SystemUser


@dataclass
class Profile:

    def __init__(self):
        self._session_username: str = session['username']

    def user_details(self):
        # user_record = db.session.query(SystemUser).filter_by(email=self.user_session).first()
        user_record = db.session.execute(db.select(SystemUser).filter_by(email=self._session_username)).scalar_one()
        return user_record

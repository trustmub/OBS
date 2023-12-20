from abc import ABC
from dataclasses import dataclass

from flask import session

from src import db
from src.models.system_user_model import SystemUser


@dataclass
class Profile(ABC):

    def __init__(self):
        self._session_username: str = session['username']

    def user_details(self) -> SystemUser:
        user_record: SystemUser = db.session.execute(
            db.select(SystemUser).filter_by(email=self._session_username)).scalar_one()
        return user_record

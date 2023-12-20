from flask import session

from src.models.system_user_model import SystemUser
from src import db


class DashboardRepository:

    def __init__(self):
        self._session_username: str = session['username']

    def get_current_user_details(self) -> SystemUser:
        user_record: SystemUser = db.session.execute(
            db.select(SystemUser).filter_by(email=self._session_username)).scalar_one()
        return user_record

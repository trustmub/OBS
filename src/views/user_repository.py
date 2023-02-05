from flask import session

from src import db
from src.models.system_user_model import SystemUser


class UserRepository:

    @staticmethod
    def query_current_system_user() -> SystemUser:
        return db.session.execute(db.select(SystemUser).filter_by(email=session["username"])).scalar_one()

    @staticmethod
    def query_system_user_by_email(email: str) -> SystemUser:
        return db.session.execute(db.select(SystemUser).filter_by(email=email)).scalar_one()

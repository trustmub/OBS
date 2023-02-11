from __future__ import annotations

from flask import session

from src import db
from src.models.system_user_model import SystemUser


class UserRepository:

    @staticmethod
    def query_system_user(email: str | None = None) -> SystemUser:
        if email is None:
            return db.session.execute(db.select(SystemUser).filter_by(email=session["username"])).scalar_one()
        else:
            return db.session.execute(db.select(SystemUser).filter_by(email=email)).scalar_one()

    @staticmethod
    def query_update_user(user: SystemUser):
        db.session.add(user)
        db.session.commit()

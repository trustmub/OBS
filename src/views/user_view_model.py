from flask import session

from src import db
from src.models.branch_model import Branch
from src.models.system_user_model import SystemUser


def get_all_branches():
    return db.session.execute(db.select(Branch).all())


def get_user_details_by_email(email: str) -> SystemUser:
    return db.session.execute(db.select(SystemUser).filter_by(email=email)).scalar_one()


def update_user_login_session(user: SystemUser, username: str) -> None:
    session['username'] = username
    user.lock = 1
    db.session.add(user)
    db.session.commit()

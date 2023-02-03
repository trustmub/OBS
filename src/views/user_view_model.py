from enum import Enum

from flask import session

from src import db
from src.controller.user import UserController
from src.forms.user_forms import LoginForm
from src.models.branch_model import Branch
from src.models.system_user_model import SystemUser


class LoginState(Enum):
    SHOW_LOGIN = 0
    SHOW_LOGIN_INCORRECT_PASSWORD = 1
    SHOW_LOGIN_EMAIL_NOT_EXIST = 2
    SHOW_LOGIN_LOCKED = 3
    SHOW_DASHBOARD = 4
    SHOW_LOGOUT = 5
    SHOW_LOGOUT_ALREADY = 6


def get_all_branches():
    return db.session.execute(db.select(Branch)).scalars()


def get_user_details_by_email(email: str) -> SystemUser:
    return db.session.execute(db.select(SystemUser).filter_by(email=email)).scalar_one()


def update_user_login_session(user: SystemUser, username: str) -> None:
    session['username'] = username
    user.lock = 1
    db.session.add(user)
    db.session.commit()


def process_login(form: LoginForm) -> LoginState:
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user_instance = UserController(email=email, password=password)
        if user_instance.verify_email():
            user_account = get_user_details_by_email(email)

            if user_account.lock == 1:  # Checker.userDbSession(email):
                return LoginState.SHOW_LOGIN_LOCKED
            else:
                if user_instance.verify_password():
                    update_user_login_session(user_account, email)
                    return LoginState.SHOW_DASHBOARD
                else:
                    return LoginState.SHOW_LOGIN_INCORRECT_PASSWORD
        else:
            return LoginState.SHOW_LOGIN_EMAIL_NOT_EXIST

    return LoginState.SHOW_LOGIN


def process_logout() -> LoginState:
    if 'username' in session:
        login_user = session['username']
        user_account = db.session.query(SystemUser).filter_by(email=login_user).first()
        user_account.lock = 0
        db.session.add(user_account)
        db.session.commit()
        session.pop('username', None)
        return LoginState.SHOW_LOGOUT
    else:
        return LoginState.SHOW_LOGOUT_ALREADY

import os
import random
import string
from enum import Enum
from typing import List, Tuple, Any

from flask import session
from PIL import Image

from src.controller.base_repository import BaseRepository
from src.controller.user_controller import UserController
from src.forms.user_forms import LoginForm, LockScreenForm, RegistrationsForm, UserProfileForm
from src.models.branch_model import Branch
from src.models.system_user_model import SystemUser
from src.views.user_repository import UserRepository

UPLOAD_FOLDER = os.path.abspath("src/static/img/user///")

user_repository = UserRepository()
base_repository = BaseRepository()


class LoginState(Enum):
    SHOW_LOGIN = 0
    SHOW_LOGIN_INCORRECT_PASSWORD = 1
    SHOW_LOGIN_EMAIL_NOT_EXIST = 2
    SHOW_LOGIN_LOCKED = 3
    SHOW_DASHBOARD = 4
    SHOW_LOGOUT = 5
    SHOW_LOGOUT_ALREADY = 6
    SHOW_LOGIN_LOCKSCREEN = 7
    SHOW_LOCKSCREEN = 8
    SHOW_REGISTER = 9
    SHOW_USER_PROFILE = 10
    SHOW_USER_EDIT_PROFILE = 11


def get_profile_user_details() -> SystemUser:
    return user_repository.query_system_user()


def get_all_branches() -> List[Branch]:
    return base_repository.get_branches()


def _get_user_details_by_email(email: str) -> SystemUser:
    return user_repository.query_system_user(email)


def _get_current_system_user() -> SystemUser:
    return user_repository.query_system_user()


def update_user_login_session(user: SystemUser, username: str) -> None:
    session['username'] = username
    user.lock = 1
    user_repository.query_update_user(user)


def _generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def save_image(form_picture):
    """
    saves the form_picture object with new randomly generated name and scales the image to 125 x 125 using
    the Pillow image library

    params:
        form_picture: is an object of type <class 'werkzeug.datastructures.FileStorage'>
    return:
        a string for the new image filename
    """
    random_hex = _generate_random_key(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    image_filename = random_hex + f_ext

    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

    output_size = (125, 125)
    resize_image = Image.open(form_picture)
    resize_image.thumbnail(output_size)
    resize_image.save(image_path)
    return image_filename


def process_edit_profile(form: UserProfileForm):
    form.branch_code.choices = [(t.code, t.description) for t in get_all_branches()]
    if form.validate_on_submit():
        image_file = ''
        if form.image_string.data:
            image_file = save_image(form.image_string.data)

        user = user_repository.query_system_user()
        user_controller = UserController(user.email, 'blank',
                                         form.full_name.data,
                                         form.job_title.data,
                                         image_file,
                                         form.department.data,
                                         form.branch_code.data,
                                         form.access_level.data)
        user_controller.update_user()
        return LoginState.SHOW_USER_PROFILE
    return LoginState.SHOW_USER_EDIT_PROFILE


def _set_user_lock_state(lock: bool, user: SystemUser) -> None:
    user.lock = 1 if lock else 0
    user_repository.query_update_user(user)


def process_lock_screen(form: LockScreenForm) -> tuple[LoginState, Any]:
    user_account: SystemUser = user_repository.query_system_user()

    if form.validate_on_submit():
        password = form.password.data

        user_instance = UserController(full_name=user_account.full_name, email=user_account.email, password=password)

        if user_instance.verify_password():
            _set_user_lock_state(True, user_account)
            return LoginState.SHOW_DASHBOARD, None
        else:
            return LoginState.SHOW_LOGIN_LOCKSCREEN, None
    else:
        _set_user_lock_state(False, user_account)
        return LoginState.SHOW_LOCKSCREEN, user_account


def process_login(form: LoginForm) -> LoginState:
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user_instance = UserController(email=email, password=password)
        if user_instance.verify_email():
            user_account = _get_user_details_by_email(email)

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
        user_account = user_repository.query_system_user()
        _set_user_lock_state(False, user_account)
        session.pop('username', None)
        return LoginState.SHOW_LOGOUT
    else:
        return LoginState.SHOW_LOGOUT_ALREADY


def process_register(form: RegistrationsForm) -> LoginState:
    if form.validate_on_submit():
        full_name = form.fullname.data
        email = form.email.data
        password = form.password.data
        ts_and_cs = form.ts_and_cs.data
        user_controller = UserController(full_name=full_name, email=email, password=password)
        user_controller.add_new_user()
        return LoginState.SHOW_LOGIN
    else:
        return LoginState.SHOW_REGISTER

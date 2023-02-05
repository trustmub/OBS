from flask import Blueprint, render_template, redirect, url_for, flash

from src.forms.user_forms import RegistrationsForm, LoginForm, UserProfileForm, LockScreenForm
from .user_view_model import get_all_branches, process_login, \
    LoginState, process_logout, process_lock_screen, process_register, process_edit_profile, get_profile_user_details

user_view = Blueprint('user_view', __name__)


# bcrypt = Bcrypt()


@user_view.route('/lockscreen/', methods=['post', 'get'])
def lockscreen():
    form = LockScreenForm()

    state = process_lock_screen(form)
    if state[0] == LoginState.SHOW_DASHBOARD:
        return redirect(url_for('dashboard_view.home'))
    elif state[0] == LoginState.SHOW_LOGIN_LOCKSCREEN:
        flash("Wrong Password try again", "danger")
        return redirect(url_for('user_view.lockscreen'))
    elif state[0] == LoginState.SHOW_LOCKSCREEN:
        return render_template('user/lockscreen.html', user=state[1], form=form)


@user_view.route('/', methods=['POST', 'GET'])
def login():
    """
    This function handles the login requests by the user. it takes in the email and password as
    input parameters
    :return: template and form
    """
    form = LoginForm()

    state = process_login(form)
    if state == LoginState.SHOW_LOGIN:
        return render_template('user/login.html', form=form)
    elif state == LoginState.SHOW_LOGIN_LOCKED:
        flash('User is locked, Contact Systems Administrator', 'danger')
        return redirect(url_for('user_view.login'))
    elif state == LoginState.SHOW_LOGIN_INCORRECT_PASSWORD:
        flash('Password is Incorrect', 'danger')
        return redirect(url_for('user_view.login'))
    elif state == LoginState.SHOW_LOGIN_EMAIL_NOT_EXIST:
        flash('Email does not exist', 'warning')
        return redirect(url_for('user_view.login'))
    elif state == LoginState.SHOW_DASHBOARD:
        return redirect(url_for('dashboard_view.home'))


@user_view.route('/register', methods=['POST', 'GET'])
def register():
    """
    this function handles the registration of a new user
    :return:
        render_template and form
    """
    form = RegistrationsForm()
    state = process_register(form)
    if state == LoginState.SHOW_LOGIN:
        flash('User Successfully Registered', 'success')
        return redirect(url_for('user_view.login'))
    elif state == LoginState.SHOW_REGISTER:
        return render_template('user/register.html', form=form)


@user_view.route('/logout/')
def logout():
    state = process_logout()
    if state == LoginState.SHOW_LOGOUT:
        flash("Logged Out", "success")
        return redirect(url_for('user_view.login'))
    else:
        flash('Already Logged Off', 'warning')
        return redirect(url_for('user_view.login'))


#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_view.route('/edit_user/', methods=['POST', 'GET'])
def edit_profile():
    form = UserProfileForm()

    state = process_edit_profile(form)
    if state == LoginState.SHOW_USER_PROFILE:
        return redirect(url_for('user_view.profile', user=get_profile_user_details()))
    elif state == LoginState.SHOW_USER_EDIT_PROFILE:
        return render_template('user/edit_user.html', user=get_profile_user_details(), branch=get_all_branches(),
                               form=form)


@user_view.route('/admin')
def test_admin():
    return render_template('user/test_admin.html')


@user_view.route('/profile/')
def profile():
    return render_template('user/profile.html', user=get_profile_user_details())

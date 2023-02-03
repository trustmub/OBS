import os
import random
# import secrets
import string

from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, session

from src import db
from src.controller.user import UserController
from src.forms.user_forms import RegistrationsForm, LoginForm, UserProfileForm, LockScreenForm
from src.functions.user_profile import Profile
from src.models.system_user_model import SystemUser
from .user_view_model import get_all_branches, get_user_details_by_email, update_user_login_session, process_login, \
    LoginState, process_logout

UPLOAD_FOLDER = os.path.abspath("src/static/img/user///")

user_view = Blueprint('user_view', __name__)


# bcrypt = Bcrypt()


@user_view.route('/lockscreen/', methods=['post', 'get'])
def lockscreen():
    form = LockScreenForm()

    if form.validate_on_submit():
        password = form.password.data
        email = session['username']

        # user_account = session.query(User).filter_by(email=email).first()
        user_account = db.session.query(SystemUser).filter_by(email=email).first()

        user_instance = UserController(full_name=user_account.full_name,
                                       email=email,
                                       password=password)

        if user_instance.verify_password():
            user_account.lock = 1
            db.session.add(user_account)
            db.session.commit()
            return redirect(url_for('dashboard_view.home'))
        else:
            flash("Wrong Password try again", "danger")
            return redirect(url_for('user_view.lockscreen'))
    else:
        user_session = session['username']
        # user_account = session.query(User).filter_by(email=user_session).first()
        user_account = db.session.query(SystemUser).filter_by(email=user_session).first()
        user_account.lock = 0
        db.session.add(user_account)
        db.session.commit()

        return render_template('user/lockscreen.html', user=user_account, form=form)


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
    if form.validate_on_submit():
        full_name = form.fullname.data
        email = form.email.data
        password = form.password.data
        ts_and_cs = form.ts_and_cs.data
        record = UserController(full_name=full_name, email=email, password=password)
        record.add_new_user()
        flash('User Successfully Registered', 'success')
        return redirect(url_for('user_view.login'))
    else:
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

def generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def save_image(form_picture):
    """
    saves the form_picture object with new randomly generated name and scales the image to 125 x 125 using
    the Pillow image library

    :param
        form_picture: is an object of type <class 'werkzeug.datastructures.FileStorage'>
    :return:
        a string for the new image filename
    """
    random_hex = generate_random_key(8)

    _, f_ext = os.path.splitext(form_picture.filename)
    image_filename = random_hex + f_ext

    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

    output_size = (125, 125)
    resize_image = Image.open(form_picture)
    resize_image.thumbnail(output_size)
    resize_image.save(image_path)
    return image_filename


@user_view.route('/edit_user/', methods=['POST', 'GET'])
def edit_profile():
    form = UserProfileForm()
    form.branch_code.choices = [(t.code, t.description) for t in get_all_branches()]
    if form.validate_on_submit():
        image_file = ''
        if form.image_string.data:
            image_file = save_image(form.image_string.data)

        usr = Profile().user_details()
        user_controller = UserController(usr.email, 'blank',
                                         form.full_name.data,
                                         form.job_title.data,
                                         image_file,
                                         form.department.data,
                                         form.branch_code.data,
                                         form.access_level.data)
        user_controller.update_user()
        print("all is valid")
        return redirect(url_for('user_view.profile',
                                user=Profile().user_details()))
    print("reloaded")
    return render_template('user/edit_user.html',
                           user=Profile().user_details(),
                           branch=get_all_branches(), form=form)


@user_view.route('/admin')
def test_admin():
    return render_template('user/test_admin.html')


@user_view.route('/profile/')
def profile():
    return render_template('user/profile.html', user=Profile().user_details())

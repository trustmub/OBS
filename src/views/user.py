import os
import secrets
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_bcrypt import Bcrypt
from PIL import Image
from werkzeug.utils import secure_filename

from src import login_manager
from src.forms.user_forms import RegistrationsForm, LoginForm, UserProfileForm, LockScreenForm
from src.controller.user import UserController

from src.utilities.verifier import Verify
from src.functions.genarators import *

UPLOAD_FOLDER = os.path.abspath("src/static/img/user///")

user_view = Blueprint('user_view', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bcrypt = Bcrypt()


@user_view.route('/lockscreen/', methods=['post', 'get'])
def lockscreen():
    form = LockScreenForm()

    if form.validate_on_submit():
        password = form.password.data
        email = login_session['username']

        user_account = session.query(User).filter_by(email=email).first()

        user_instance = UserController(full_name=user_account.full_name,
                                       email=email,
                                       password=password)

        if user_instance.verify_password():
            user_account.lock = 1
            session.add(user_account)
            session.commit()
            return redirect(url_for('home'))
        else:
            flash("Wrong Password try again", "danger")
            return redirect(url_for('user_view.lockscreen'))
    else:
        user_session = login_session['username']
        user_account = session.query(User).filter_by(email=user_session).first()
        user_account.lock = 0
        session.add(user_account)
        session.commit()

        return render_template('user/lockscreen.html', user=user_account, form=form)


@user_view.route('/', methods=['POST', 'GET'])
def login():
    """
    This function handles the login requests by the user. it takes in the email and password as
    input parameters
    :return: template and form
    """
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user_instance = UserController(email=email, password=password)
        if user_instance.verify_email():
            user_account = session.query(User).filter_by(email=email).first()

            if user_account.lock == 1:  # Checker.userDbSession(email):
                flash('User is locked, Contact Systems Administrator', 'danger')
                return redirect(url_for('user_view.login'))
            else:
                if user_instance.verify_password():
                    login_session['username'] = email

                    user_account.lock = 1
                    session.add(user_account)
                    session.commit()
                    return redirect(url_for('home'))
                else:
                    flash('Password is Incorrect', 'danger')
                    return redirect(url_for('user_view.login'))
        else:
            flash('Email does not exist', 'warning')
            return redirect(url_for('user_view.login'))

    return render_template('user/login.html', form=form)


@user_view.route('/register/', methods=['POST', 'GET'])
def register():
    """
    this function handles the registration of a new user
    :return:
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
    if 'username' in login_session:
        login_user = login_session['username']
        user_account = session.query(User).filter_by(email=login_user).first()
        user_account.lock = 0
        session.add(user_account)
        session.commit()
        login_session.pop('username', None)
        flash("Logged Out", "success")
        return redirect(url_for('user_view.login'))
    else:
        flash('Already Logged Off', 'warning')
        return redirect(url_for('user_view.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(form_picture):
    """
    function saves the passes image callable to a specified file path (imafe_path) the file is renamed
    to an 8 byte name using the secrets.token_hex function. the file is resized to 125 x 125 using
    the Pillow image library

    The returned filename is saved on the database.

    :param form_picture:
    :return: image_filename
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    output_size = (125,125)
    resize_image = Image.open(form_picture)
    resize_image.thumbnail(output_size)
    resize_image.save(image_path)
    return image_filename


@user_view.route('/edit_user/', methods=['POST', 'GET'])
def edit_profile():
    form = UserProfileForm()
    form.branch_code.choices = [(t.code, t.description) for t in Getters.getBranch()]
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
                           branch=Getters.getBranch(), form=form)


@user_view.route('/admin')
def test_admin():
    return render_template('user/test_admin.html')


@user_view.route('/profile/')
def profile():
    return render_template('user/profile.html', user=Profile().user_details())

import os
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from src import login_manager
from src.forms.user_forms import RegistrationsForm, LoginForm, UserProfileForm, LockScreenForm
from src.controller.user import UserController

from src.utilities.verifier import Verify
from src.functions.genarators import *

UPLOAD_FOLDER = os.path.abspath("static//img//user")

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


@user_view.route('/edit_user/', methods=['POST', 'GET'])
def edit_profile():
    form = UserProfileForm()
    if request.method == 'POST':
        user_details = Profile().user_details()
        if request.form['full_name'] == user_details.full_name:
            pass
        else:
            user_details.full_name = request.form['full_name']
        if request.form['job_title'] == user_details.job_title:
            pass
        else:
            user_details.job_title = request.form['job_title']
        if request.form['department'] == user_details.department:
            pass
        else:
            user_details.department = request.form['department']
        if request.form['branch_code'] == user_details.branch_code:
            pass
        else:
            user_details.branch_code = request.form['branch_code']
        if request.form['access_level'] == user_details.access_level:
            pass
        else:
            user_details.access_level = request.form['access_level']

        if request.files['image_string'].filename == user_details.image_string:
            pass
        else:
            user_details.image_string = secure_filename(request.files['image_string'].filename)
            file = request.files['image_string']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                print(UPLOAD_FOLDER)
        session.add(user_details)
        session.commit()
        return redirect(url_for('user_view.profile',
                                user=Profile().user_details()))
    else:
        return render_template('user/edit_user.html',
                               user=Profile().user_details(),
                               branch=Getters.getBranch())


@user_view.route('/admin')
def test_admin():
    return render_template('user/test_admin.html')


@user_view.route('/profile/')
def profile():
    return render_template('user/profile.html', user=Profile().user_details())

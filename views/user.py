from flask import Blueprint, render_template, redirect, request, url_for
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from controller.verifier import Verify
from functions.genarators import *

UPLOAD_FOLDER = os.path.abspath("static//img//user")

user = Blueprint('user', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bcrypt = Bcrypt()


@user.route('/lockscreen/', methods=['post', 'get'])
def lockscreen():
    if request.method == 'POST':
        password = request.form['password']
        email = login_session['username']
        user_account = session.query(User).filter_by(email=email).first()
        if bcrypt.check_password_hash(user_account.password, password):
            user_account.lock = 1
            session.add(user_account)
            session.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('user.lockscreen'))
    else:
        user_session = login_session['username']
        user_account = session.query(User).filter_by(email=user_session).first()
        user_account.lock = 0

        return render_template('user/lockscreen.html', user=user_account)


@user.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'username' in login_session:
            flash('User already Logged in')
            return redirect(url_for('user.login'))
        else:
            email = request.form['email']
            password = request.form['password']
            if Verify().email_exists(email):
                user_account = session.query(User).filter_by(email=email).first()
                # user_account.lock = 0
                if user_account.lock == 1:  # Checker.userDbSession(email):
                    flash('User is locked, Contact Systems Administrator')
                    return redirect(url_for('user.login'))
                else:
                    if bcrypt.check_password_hash(user_account.password, password):
                        login_session['username'] = email

                        user_account.lock = 1
                        session.add(user_account)
                        session.commit()
                        return redirect(url_for('home'))
                    else:
                        flash('Password is Incorrect')
                        return redirect(url_for('user.login'))
            else:
                flash('Email does not exist')
                return redirect(url_for('user.login'))
    else:
        return render_template('user/login.html')


@user.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password2']
        if password != password_confirm:
            flash('Passwords Don\'t match')
            return redirect(url_for('user.register'))
        elif Verify().email_exists(email):
            flash('User Already Exists')
            return redirect(url_for('user.register'))
        else:
            new = User(full_name=full_name,
                       job_title='',
                       image_string='',
                       department='',
                       branch_code='',
                       access_level=0,
                       till_o_balance=0,
                       till_c_balance=0,
                       create_date=datetime.datetime.now(),
                       email=email,
                       password=bcrypt.generate_password_hash(password, 12),
                       lock=0)
            session.add(new)
            session.commit()
            flash('User Successfully Registered')
            return redirect(url_for('user.login'))
    else:
        return render_template('user/register.html')


@user.route('/logout/')
def logout():
    if 'username' in login_session:
        login_user = login_session['username']
        user_account = session.query(User).filter_by(email=login_user).first()
        user_account.lock = 0
        session.add(user_account)
        session.commit()
        login_session.pop('username', None)
        flash("Logged Out")
        return redirect(url_for('user.login'))
    else:
        flash('Already Logged Off')
        return redirect(url_for('user.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user.route('/edit_user/', methods=['POST', 'GET'])
def edit_profile():
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
        return redirect(url_for('user.profile', user=Profile().user_details()))
    else:
        return render_template('user/edit_user.html', user=Profile().user_details(), branch=Getters.getBranch())


@user.route('/admin')
def test_admin():
    return render_template('user/test_admin.html')


@user.route('/profile/')
def profile():
    return render_template('user/profile.html', user=Profile().user_details())

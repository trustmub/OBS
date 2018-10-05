import datetime
from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .functions.genarators import Getters, session, User, Profile


APP = Flask(__name__)
APP.secret_key = 'asdkerhg8927qr9w0rhgwe70gw9eprg7w0e9r7g'

bcrypt = Bcrypt(APP)

login_manager = LoginManager(APP)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from .views.user import user_view
from .views.banking import banking
from .views.customer import customer
from .views.till import till
from .views.settings import settings
from .views.recon import reconciliation
from .views.enquiry import enquiry
from .views.bulk import bulk
from .api.api import bank_api

APP.register_blueprint(user_view)
APP.register_blueprint(banking)
APP.register_blueprint(customer)
APP.register_blueprint(till)
APP.register_blueprint(reconciliation)
APP.register_blueprint(enquiry)
APP.register_blueprint(bulk)
APP.register_blueprint(settings)
APP.register_blueprint(bank_api)


@APP.route('/dashboard/')
def home():
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')

    usr = session.query(User).all()
    # interest = session.query(Interest).all()
    return render_template('dashboard.html',
                           usr=usr,
                           user=Profile().user_details(),
                           teller=Getters.getTillDetails(),
                           withd=Getters.getTellerWithdrawal(),
                           deposits=Getters.getTellerDeposits(),
                           sys_date=sys_date.strftime('%d %B %Y'))


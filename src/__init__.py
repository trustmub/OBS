import os

from flask import Flask
# from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.secret_key = 'asdkerhg8927qr9w0rhgwe70gw9eprg7w0e9r7g'

# basedir = os.path.abspath(os.path.dirname(__file__))
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bankbase.db')
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/bankbase'

"""user the config below to connect to mysql docker instance from local run"""
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@0.0.0.0:3306/bank_database?charset=utf8mb4'

"""user the config below to connect to mysql docker instance when running the project from docker compose"""
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@mysql-db:3306/bank_database?charset=utf8mb4'

bcrypt = Bcrypt(APP)
db = SQLAlchemy(APP)
# ma = Marshmallow(APP)

# login_manager = LoginManager(APP)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'


from .views.user import user_view
from .views.dashboard import dashboard_view
from .setup_system_params import cmd
from .views.banking import banking
from .views.customer import customer
from .views.till import till
from .views.settings import settings
from .views.recon import reconciliation
from .views.enquiry import enquiry
from .views.bulk import bulk
from .views.end_of_day import eod_view

# from .api.api import bank_api

APP.register_blueprint(user_view)
APP.register_blueprint(dashboard_view)
APP.register_blueprint(cmd)
APP.register_blueprint(banking)
APP.register_blueprint(customer)
APP.register_blueprint(till)
APP.register_blueprint(reconciliation)
APP.register_blueprint(enquiry)
APP.register_blueprint(bulk)
APP.register_blueprint(settings)
APP.register_blueprint(eod_view)
# APP.register_blueprint(bank_api)

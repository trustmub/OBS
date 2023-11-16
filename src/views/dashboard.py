import datetime

from flask import render_template, Blueprint

from src import db
from src.functions.genarators import Getters
from src.functions.user_profile import Profile
from src.models.system_user_model import SystemUser

dashboard_view = Blueprint('dashboard_view', __name__)


@dashboard_view.route('/dashboard/')
def home():
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')

    # usr = session.query(User).all()
    usr = db.session.query(SystemUser).all()
    # interest = session.query(Interest).all()
    return render_template('dashboard.html',
                           usr=usr,
                           user=Profile().user_details(),
                           teller=Getters.get_till_details(),
                           withd=Getters.getTellerWithdrawal(),
                           deposits=Getters.getTellerDeposits(),
                           sys_date=sys_date.strftime('%d %B %Y'))
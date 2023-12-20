import datetime

from flask import render_template, Blueprint, session

from src import db
from src.utils.genarators import Getters
from src.utils.system import SystemUtil
from src.utils.user_profile import Profile
from src.models.system_user_model import SystemUser
from src.views.dashboard_repository import DashboardRepository
from src.views.till_repository import TillRepository

dashboard_view = Blueprint('dashboard_view', __name__)


@dashboard_view.route('/dashboard/')
def home():
    sys_date = datetime.datetime.strptime(SystemUtil.get_system_date().date, '%Y-%m-%d')
    repository: DashboardRepository = DashboardRepository()

    current_user: SystemUser = repository.get_current_user_details()
    till_details: TillRepository = TillRepository.get_till_details_by_user_id(current_user.uid)

    # usr = session.query(User).all()
    usr = db.session.query(SystemUser).all()
    # interest = session.query(Interest).all()
    return render_template('dashboard.html',
                           usr=usr,
                           user=current_user,
                           teller=till_details,
                           withd=Getters.getTellerWithdrawal(),
                           deposits=Getters.getTellerDeposits(),
                           sys_date=sys_date.strftime('%d %B %Y'))
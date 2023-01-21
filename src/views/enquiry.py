from flask import Blueprint, render_template

from src.functions.genarators import Getters
from src.functions.user_profile import Profile

enquiry = Blueprint('enquiry', __name__)


@enquiry.route('/account_reset/')
def account_reset():
    record = []
    return render_template('enquiry/account_reset.html', record=record, user=Profile().user_details())


@enquiry.route('/stmt_drill_down/<ft_reference>')
def stmt_drill_down(ft_reference):
    # record = []
    record = Getters.getTransactionDetails(ft_reference)
    return render_template('enquiry/stmt_drilldown.html', record=record, user=Profile().user_details())

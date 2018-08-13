from flask import Blueprint, render_template, redirect, request, url_for, flash

from src.functions.genarators import Profile, Getters

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

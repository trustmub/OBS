import time

from flask import Blueprint, render_template, request, url_for, redirect, flash, session

# from src import db
from src.controller.till import TillController
from src.forms.till_forms import OpenTillForm
from src.utils.Enums import TransactionType
from src.utils.genarators import Getters, TransactionUpdate
from src.utils.queries import Query
from src.utils.system import SystemUtil
from src.utils.user_profile import Profile
from src.models.customer_model import Customer
from src.models.till_model import Till
from src.views.till_repository import TillRepository

till = Blueprint('till', __name__)


@till.route('/my_till/')
def my_till():
    return render_template('till/my_till.html', user=Profile().user_details())


# @till.route('/open_till/', methods=['POST', 'GET'])
# def open_till():
#     form = OpenTillForm()
#     form.teller_num.choices = [(str(t.id), t.id) for t in Query().available_tellers()]
#     form.branch.choices = [(b.code, b.description) for b in Getters.getBranch()]
#
#     if form.validate_on_submit():
#         print("branch code: {}".format(form.branch.data))
#         print("opening balance: {}".format(form.o_balance.data))
#         print("user ID: {}".format(form.user_id.data))
#         print("till number: {}".format(form.teller_num.data))
#
#         till_controller = TillController(branch_code=form.branch.data,
#                                          o_balance=form.o_balance.data,
#                                          user_id=form.user_id.data,
#                                          teller_id=form.teller_num.data)
#         till_controller.open_till()
#
#         return redirect(url_for('till.open_till'))
#
#     else:
#         if current user_view has a till linked, display the till detail
#         else display the general till opening
#         if form.errors:
#             print(form.errors)
#         return render_template('till/open_till.html', user=Profile().user_details(),
#                                branch=Getters.getBranch(),
#                                teller2=Getters.getAllTellers(),
#                                teller_linked=Query().teller_status(),
#                                form=form)
@till.route('/open_till/', methods=['POST', 'GET'])
def open_till():
    form = OpenTillForm()
    form.teller_num.choices = [(str(t.id), t.id) for t in Query().available_tellers()]
    form.branch.choices = [(b.code, b.description) for b in SystemUtil.get_system_branches()]

    if form.validate_on_submit():
        branch_code = form.branch.data
        o_balance = form.o_balance.data
        user_id = form.user_id.data
        teller_num = form.teller_num.data

        till_controller = TillController(branch_code=branch_code,
                                         opening_balance=o_balance,
                                         user_id=user_id,
                                         teller_id=teller_num)
        till_controller.open_till()

        return redirect(url_for('till.open_till'))

    else:
        form_errors = form.errors or {}
        print(form_errors)

        user_details = Profile().user_details()
        branches = SystemUtil.get_system_branches()
        tellers = Getters.getAllTellers()
        teller_linked = Query().teller_status()

        return render_template('till/open_till.html',
                               user=user_details,
                               branch=branches,
                               teller2=tellers,
                               teller_linked=teller_linked,
                               form=form)


@till.route('/close_till/', methods=['POST', 'GET'])
def close_till():
    if request.method == 'POST':
        total_deposits = float(request.form['total_deposits'])
        total_withdrawals = float(request.form['total_withdrawals'])
        cash_on_hand = float(request.form['coh'])
        if total_deposits == Getters.getTellerDeposits():
            if total_withdrawals == Getters.getTellerWithdrawal():
                till_details = TillRepository.get_till_details_by_session(session["username"])  # Getters.get_till_details()
                sys_balance = till_details.opening_balance - till_details.closing_balance
                if cash_on_hand == sys_balance:
                    TillRepository.close_till(sys_balance)
                    flash('Till Closed Successfully')
                    return redirect(url_for('till.close_till'))
                else:
                    flash('Cash.On.Hand DOES NOT Tally With The System')
                    return redirect(url_for('till.close_till'))
            else:
                flash('Withdrawals DO NOT Tally With The System')
                return redirect(url_for('till.close_till'))
        else:
            flash('Deposits DO NOT Tally With The System')
            return redirect(url_for('till.close_till'))
        pass
    else:
        return render_template('till/close_till.html', user=Profile().user_details(), my_till=TillRepository.get_till_details_by_session(session["username"]),
                               my_tt=Getters.getTellerTransactions(), teller_linked=Getters.getTellerStatus())

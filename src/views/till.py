import time

from flask import Blueprint, render_template, request, url_for, redirect, flash

from src import db
from src.controller.till import TillController
from src.forms.till_forms import OpenTillForm
from src.functions.Enums import TransactionType
from src.functions.genarators import Getters, TransactionUpdate
from src.functions.queries import Query
from src.functions.user_profile import Profile
from src.models.customer_model import Customer
from src.models.till_model import Till

till = Blueprint('till', __name__)


@till.route('/my_till/')
def my_till():
    return render_template('till/my_till.html', user=Profile().user_details())


@till.route('/open_till/', methods=['POST', 'GET'])
def open_till():
    form = OpenTillForm()
    form.teller_num.choices = [(str(t.id), t.id) for t in Query().available_tellers()]
    form.branch.choices = [(b.code, b.description) for b in Getters.getBranch()]

    if form.validate_on_submit():
        print("branch code: {}".format(form.branch.data))
        print("opening balance: {}".format(form.o_balance.data))
        print("user ID: {}".format(form.user_id.data))
        print("till number: {}".format(form.teller_num.data))

        till_controller = TillController(branch_code=form.branch.data,
                                         o_balance=form.o_balance.data,
                                         user_id=form.user_id.data,
                                         teller_id=form.teller_num.data)
        till_controller.open_till()

        return redirect(url_for('till.open_till'))

    else:
        # if current user_view has a till linked, display the till detail
        # else display the general till opening
        if form.errors:
            print(form.errors)
        return render_template('till/open_till.html', user=Profile().user_details(),
                               branch=Getters.getBranch(),
                               teller2=Getters.getAllTellers(),
                               teller_linked=Query().teller_status(),
                               form=form)


@till.route('/close_till/', methods=['POST', 'GET'])
def close_till():
    if request.method == 'POST':
        total_deposits = float(request.form['total_deposits'])
        total_withdrawals = float(request.form['total_withdrawals'])
        coh = float(request.form['coh'])
        if total_deposits == Getters.getTellerDeposits():
            if total_withdrawals == Getters.getTellerWithdrawal():
                gtd = Getters.getTillDetails()
                sys_balance = gtd.o_balance - gtd.c_balance
                if coh == sys_balance:  # opening balance - closing balance
                    # send cash back to suspense account
                    #  tt transaction
                    suspense = db.session.query(Customer).filter_by(account_type='suspense').first()
                    TransactionUpdate.ttUpdate(TransactionType.CR_DR, sys_balance, time.strftime('%Y-%m-%d'),
                                               'Closing Balance',
                                               suspense.acc_number)
                    till_detail = db.session.query(Till).filter_by(
                        till_account=Getters.getTillDetails().till_account).first()
                    till_detail.c_balance = 0
                    till_detail.o_balance = 0
                    till_detail.user_id = ''
                    db.session.add(till_detail)
                    db.session.commit()
                    # Credit suspense account with the closing balanced figure
                    suspense.working_bal += sys_balance
                    db.session.add(suspense)
                    db.session.commit()

                    # move the cash in the teller opening balance to closing balance
                    #
                    flash('Till Closed Successfully')
                    return redirect(url_for('till.close_till'))
                else:
                    flash('C.O.H DOES NOT Tally With The System')
                    return redirect(url_for('till.close_till'))
            else:
                flash('Withdrawals DO NOT Tally With The System')
                return redirect(url_for('till.close_till'))
        else:
            flash('Deposits DO NOT Tally With The System')
            return redirect(url_for('till.close_till'))
        pass
    else:
        return render_template('till/close_till.html', user=Profile().user_details(), my_till=Getters.getTillDetails(),
                               my_tt=Getters.getTellerTransactions(), teller_linked=Getters.getTellerStatus())

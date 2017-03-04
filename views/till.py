import time
import datetime

from flask import Blueprint, render_template, request, url_for, redirect

from functions.genarators import *

till = Blueprint('till', __name__)


@till.route('/my_till/')
def my_till():
    return render_template('till/my_till.html', user=Nav.userDetails())


@till.route('/open_till/', methods=['POST', 'GET'])
def open_till():
    if request.method == 'POST':
        till_num = int(request.form['teller_num'])
        branch_code = request.form['branch_code']
        o_balance = float(request.form['o_balance'])
        user_id = int(request.form['user_id'])
        till_record = session.query(Till).filter_by(id=till_num).first()

        till_record.branch_code = branch_code
        till_record.o_balance = o_balance
        till_record.user_id = user_id
        till_record.date = time.strftime('%Y-%m-%d')

        session.add(till_record)
        session.commit()
        # do a till transaction in creadditing the till and affecting the suspense account
        suspense = session.query(Customer).filter_by(account_type='suspense').first()
        TransactionUpdate.ttUpdate('CR TR', o_balance, time.strftime('%Y-%m-%d'), 'Teller Transfer', suspense.acc_number)
        # ------------------------

        # Update the working balance of the suspense account
        suspense.working_bal -= o_balance
        session.add(suspense)
        session.commit()
        # ---------------------------------------------------

        return redirect(url_for('home'))

    else:
        # if current user has a till linked, display the till detail
        # else display the general till opening
        return render_template('till/open_till.html', user=Nav.userDetails(),
                               branch=Getters.getBranch(), teller=Getters.getAvailableTellers(),
                               teller2=Getters.getAllTellers(), ts=Getters.getTellerStatus())


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
                    suspense = session.query(Customer).filter_by(account_type='suspense').first()
                    TransactionUpdate.ttUpdate('DR TR', sys_balance, time.strftime('%Y-%m-%d'), 'Closing Balance',
                                               suspense.acc_number)
                    till_detail = session.query(Till).filter_by(
                        till_account=Getters.getTillDetails().till_account).first()
                    till_detail.c_balance = 0
                    till_detail.o_balance = 0
                    till_detail.user_id = ''
                    session.add(till_detail)
                    session.commit()
                    # Credit suspense account with the closing balanced figure
                    suspense.working_bal += sys_balance
                    session.add(suspense)
                    session.commit()

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
        return render_template('till/close_till.html', user=Nav.userDetails(), my_till=Getters.getTillDetails(),
                               my_tt=Getters.getTellerTransactions(), ts=Getters.getTellerStatus())

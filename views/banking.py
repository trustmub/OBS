import time

from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask import session as login_session

from utilities.search import Search
from utilities.verifier import Verify
from functions.Enums import TransactionType
from functions.genarators import Profile, Checker, Getters, TransactionUpdate, Auto
from functions.transactions import AccountTransaction, ChargeTransaction
from models.models import Customer, Banks

from models import session

banking = Blueprint('banking', __name__)


@banking.route('/dep_account_search/', methods=['post', 'get'])
def account_search():
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        record = Search().search_by_account(acc_num)
        if record is not None:
            return render_template('banking/deposits.html', record=record, user=Profile().user_details())
        else:
            flash('The Account Number Provided Is NOT In The System')
            return render_template('banking/deposits.html', record=record, user=Profile().user_details())
    else:
        return redirect(url_for('banking.deposits'))


@banking.route('/deposits/', methods=['POST', 'GET'])
def deposits():
    record = None
    if request.method == 'POST':
        if Verify().till_is_linked(login_session['username']):
            cr_account_number = int(request.form['client_account'])
            if Verify().account_exists(cr_account_number):
                system_date = Getters.getSysDate().date  # use system date for transactions
                dep_ref = request.form['deposit_ref']
                amount = float(request.form['deposit_amount'])

                AccountTransaction(date=system_date, amount=amount, cr_account=cr_account_number).deposit(dep_ref)

                TransactionUpdate.ttUpdate('DR', amount, system_date, dep_ref, cr_account_number)
                flash('Account Credited')
                return redirect(url_for('banking.deposits', user=Profile().user_details()))
            else:
                flash('Account Cannot be found: Search again')
                return redirect(url_for('banking.deposits', user=Profile().user_details()))
        else:
            flash('User is NOT linked to Any Till. Please Open a Till First')
            return redirect(url_for('banking.deposits'))
    else:
        return render_template('banking/deposits.html', record=record, user=Profile().user_details())


@banking.route('/stmt_search/', methods=['post', 'get'])
def stmt_search():
    dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
    start_date = ''
    end_date = ''
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        record, statement_records = Search().search_stmt_transactions(acc_num, start_date, end_date)

        if record is not None and statement_records:
            return render_template('banking/statement.html', record=record, stmt=statement_records, dt=dt,
                                   sd=start_date, ed=end_date, user=Profile().user_details())
        else:
            flash('The Account Number Provided Is NOT In The System')
            return render_template('banking/statement.html', record=record, stmt=statement_records, dt=dt,
                                   sd=start_date, ed=end_date, user=Profile().user_details())
    else:
        return redirect(url_for('banking.statement', dt=dt, sd=start_date, ed=end_date, user=Profile().user_details()))


@banking.route('/stmt_print/<account>/<start_date>/<end_date>')
def stmt_print(account, start_date, end_date):
    dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
    acc_num = int(account)
    start_date = start_date
    end_date = end_date
    # record = session.query(Customer).filter_by(acc_number=acc_num).first()
    record, statement_records = Search().search_stmt_transactions(acc_num, start_date, end_date)
    return render_template('banking/stmt_printed.html', record=record, stmt=statement_records, dt=dt, sd=start_date,
                           ed=end_date, user=Profile().user_details())


@banking.route('/statement/')
def statement():
    start_date, end_date = '', ''
    date_time = time.strftime('%Y-%m-%d')
    return render_template('banking/statement.html', record=None, stmt=[], dt=date_time, sd=start_date, ed=end_date,
                           user=Profile().user_details())


@banking.route('/transfer_search/', methods=['POST', 'GET'])
def transfer_search():
    if request.method == 'POST':
        from_account = request.form['from_account']
        to_account = request.form['to_account']
        if from_account == to_account:
            flash('The Accounts submitted are the same')
            return redirect(url_for('banking.transfer'))

        if Verify().account_exists(from_account):
            if Verify().account_exists(to_account):
                record = [from_account, to_account]
                return render_template('banking/transfer.html', user=Profile().user_details(), record=record,
                                       fad=Getters.getCustomerAccountDetails(from_account),
                                       tad=Getters.getCustomerAccountDetails(to_account))
            else:
                flash('To Account number is not valid')
                return redirect(url_for('banking.transfer'))
        else:
            flash('from account is not valid')
            return redirect(url_for('banking.transfer'))


@banking.route('/transfer/', methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        from_acc = request.form['from_acc']
        to_acc = request.form['to_acc']
        remark = request.form['remark']
        amount = float(request.form['amount'])
        if amount > Getters.getCustomerAccountDetails(from_acc).working_bal:
            flash('The Account ' + from_acc + ' has no overdraft facility ')
            return redirect(url_for('banking.transfer'))
        else:
            TransactionUpdate.transferTransactionUpdate(from_acc, to_acc, amount, remark, Getters.getSysDate().date)
            # TransactionUpdate.accChargeUpdate('TR', from_acc, Getters.getSysDate().date)
            ChargeTransaction(Getters.getSysDate().date, from_acc).charges(TransactionType.TRANSFER)

            flash('Transfer Successful')
            return redirect(url_for('banking.transfer'))
    else:
        record = []
        fad = None
        tad = None
        return render_template('banking/transfer.html', user=Profile().user_details(), record=record, fad=fad, tad=tad)


@banking.route('/external_transfer_search/', methods=['post', 'get'])
def external_transfer_search():
    if request.method == 'POST':
        acc_num = int(request.form['from_account'])
        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            return render_template('banking/external_transfer.html', record=Getters.getCustomerAccountDetails(acc_num),
                                   user=Profile().user_details(),
                                   banks=Getters.getBanks(), fad=Getters.getCustomerAccountDetails(acc_num))
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            return render_template('banking/deposits.html', record=record, user=Profile().user_details(),
                                   banks=Getters.getBanks())
    else:
        return redirect(url_for('banking.deposits'))


@banking.route('/external_transfer/', methods=['POST', 'GET'])
def external_transfer():
    if request.method == 'POST':
        from_acc = request.form['from_acc']
        to_bank = request.form['to_bank']
        swift = session.query(Banks).filter_by(name=to_bank).first()
        swift_code = swift.swift_code
        to_ext_acc = request.form['to_ext_acc']
        remark = request.form['remark']
        remark += " " + str(swift_code)
        amount = float(request.form['amount'])
        if amount > Getters.getCustomerAccountDetails(from_acc).working_bal:
            flash('Account Balance is Less than Required')
            return redirect(url_for('banking.external_transfer'))
        else:
            TransactionUpdate.externalTransferTransactionUpdate(from_acc, to_ext_acc, amount, remark,
                                                                Getters.getSysDate().date)

            # TransactionUpdate.accChargeUpdate('RTGS', from_acc, Getters.getSysDate().date)
            ChargeTransaction(Getters.getSysDate().date, from_acc).charges(TransactionType.RTGS)
            flash('RTGS Successful')
            return redirect(url_for('banking.external_transfer'))
    else:
        record = []
        # fad = From Account Details
        # tad = To Account Details
        fad = None
        tad = None
        return render_template('banking/external_transfer.html', fad=fad, tad=tad, record=record,
                               user=Profile().user_details(), banks=Getters.getBanks())


@banking.route('/with_account_search/', methods=['post', 'get'])
def with_account_search():
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        record = Search().search_by_account(acc_num)
        if record is not None:
            return render_template('banking/withdrawal.html', record=record, user=Profile().user_details())
        else:
            flash('The Account Number Provided Is NOT In The System')
            return render_template('banking/withdrawal.html', record=record, user=Profile().user_details())

        # if session.query(Customer).filter_by(acc_number=acc_num).first():
        #     record = session.query(Customer).filter_by(acc_number=acc_num).first()
        #     return render_template('banking/withdrawal.html', record=record, user_view=Profile().user_details())
        # else:
        #     flash('The Account Number Provided Is NOT In The System')
        #     record = None
        #     return render_template('banking/withdrawal.html', record=record, user_view=Profile().user_details())
    else:
        return redirect(url_for('banking.withdrawal'))


@banking.route('/withdrawal', methods=['POST', 'GET'])
def withdrawal():
    record = None
    if request.method == 'POST':
        if Verify().till_is_linked(login_session['username']):

            acc_num = int(request.form['client_account'])
            if Verify().account_exists(acc_num):
                date = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
                dep_ref = request.form['withdrawal_ref']
                ref = Auto.reference_string_generator()
                amount = float(request.form['withdrawal_amount'])

                # TransactionUpdate.withdrawalTransactionUpdate(date, acc_num, amount, ref)
                AccountTransaction(date, amount, acc_num).withdrawal(ref)

                # TransactionUpdate.accChargeUpdate(TransactionType.CREDIT, acc_num, date)
                ChargeTransaction(date, acc_num).charges(TransactionType.CREDIT)

                TransactionUpdate.ttUpdate(TransactionType.CREDIT, amount, date, dep_ref, acc_num)
                flash('Account Debited')
                return redirect(url_for('banking.withdrawal', user=Profile.user_details()))
            else:
                flash('Account Cannot be found: Search again')
                return redirect(url_for('banking.withdrawal', user=Profile.user_details()))
        else:
            flash('User is not linked to Any Till. Please Open a Till First')
            return redirect(url_for('banking.withdrawal', user=Profile().user_details()))
    else:
        return render_template('banking/withdrawal.html', record=record, user=Profile().user_details())

        # End of banking views

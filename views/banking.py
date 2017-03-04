import time
import datetime
import string

from flask import Blueprint, render_template, redirect, request, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functions.genarators import *
from models import Base, Customer, Transactions

banking = Blueprint('banking', __name__)

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@banking.route('/dep_account_search/', methods=['post', 'get'])
def account_search():
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            return render_template('banking/deposits.html', record=record, user=Nav.userDetails())
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            return render_template('banking/deposits.html', record=record, user=Nav.userDetails())
    else:
        return redirect(url_for('banking.deposits'))


@banking.route('/deposits/', methods=['POST', 'GET'])
def deposits():
    record = None
    if request.method == 'POST':
        if Checker.userTillLink(login_session['username']):
            acc_num = int(request.form['client_account'])
            if Checker.accNumberChecker(acc_num):
                # t_date = time.strftime('%Y-%m-%d')
                t_date = Getters.getSysDate().date  # use system date for transactions
                dep_ref = request.form['deposit_ref']
                amount = float(request.form['deposit_amount'])

                TransactionUpdate.depositTransactionUpdate(t_date, acc_num, amount, dep_ref)
                TransactionUpdate.ttUpdate('DR', amount, t_date, dep_ref, acc_num)
                flash('Account Credited')
                return redirect(url_for('banking.deposits', user=Nav.userDetails()))
            else:
                flash('Account Cannot be found: Search again')
                return redirect(url_for('banking.deposits', user=Nav.userDetails()))
        else:
            flash('User is NOT linked to Any Till. Please Open a Till First')
            return redirect(url_for('banking.deposits'))
    else:
        return render_template('banking/deposits.html', record=record, user=Nav.userDetails())


@banking.route('/stmt_search/', methods=['post', 'get'])
def stmt_search():
    dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
    start_date = ''
    end_date = ''
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            stmt = session.query(Transactions).filter(Transactions.custid == record.custid).filter(
                Transactions.tran_date >= start_date).filter(Transactions.tran_date <= end_date).order_by(
                Transactions.tranid).all()

            return render_template('banking/statement.html', record=record, stmt=stmt, dt=dt, sd=start_date,
                                   ed=end_date, user=Nav.userDetails())
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            stmt = []
            return render_template('banking/statement.html', record=record, stmt=stmt, dt=dt, sd=start_date,
                                   ed=end_date, user=Nav.userDetails())
    else:
        return redirect(url_for('banking.statement', dt=dt, sd=start_date, ed=end_date, user=Nav.userDetails()))


@banking.route('/stmt_print/<acc>/<sd>/<ed>')
def stmt_print(acc, sd, ed):
    dt = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
    acc_num = int(acc)
    start_date = sd
    end_date = ed
    record = session.query(Customer).filter_by(acc_number=acc_num).first()
    # stmt = session.query(Transactions).filter_by(acc_number=acc_num).order_by(Transactions.tranid).all()
    stmt = session.query(Transactions).filter(Transactions.custid == record.custid).filter(
        Transactions.tran_date >= start_date).filter(Transactions.tran_date <= end_date).order_by(
        Transactions.tranid).all()
    return render_template('banking/stmt_printed.html', record=record, stmt=stmt, dt=dt, sd=start_date, ed=end_date,
                           user=Nav.userDetails())


@banking.route('/statement/')
def statement():
    sd = ''
    ed = ''
    record = None
    stmt = []
    dt = time.strftime('%Y-%m-%d')
    return render_template('banking/statement.html', record=record, stmt=stmt, dt=dt, sd=sd, ed=ed,
                           user=Nav.userDetails())


@banking.route('/transfer_search/', methods=['POST', 'GET'])
def transfer_search():
    if request.method == 'POST':
        from_account = request.form['from_account']
        to_account = request.form['to_account']
        if from_account == to_account:
            flash('The Accounts submitted are the same')
            return redirect(url_for('banking.transfer'))
        else:
            if Checker.accNumberChecker(from_account):
                if Checker.accNumberChecker(to_account):
                    record = [from_account, to_account]
                    # fad -- From Accopunt Details
                    # tad -- To acc details
                    return render_template('banking/transfer.html', user=Nav.userDetails(), record=record,
                                           fad=Getters.getCustomerAccountDetails(from_account),
                                           tad=Getters.getCustomerAccountDetails(to_account))
                else:
                    flash('To Account number is not valid')
                    return redirect(url_for('banking.transfer'))
            else:
                flash('from account is not valid')
                return redirect(url_for('banking.transfer'))
    else:
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
            TransactionUpdate.accChargeUpdate('TR', from_acc, Getters.getSysDate().date)
            flash('Transfer Successful')
            return redirect(url_for('banking.transfer'))
    else:
        record = []
        fad = None
        tad = None
        return render_template('banking/transfer.html', user=Nav.userDetails(), record=record, fad=fad, tad=tad)


@banking.route('/externale_transfer_search/', methods=['post', 'get'])
def external_transfer_search():
    if request.method == 'POST':
        acc_num = int(request.form['from_account'])
        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            return render_template('banking/external_transfer.html', record=Getters.getCustomerAccountDetails(acc_num),
                                   user=Nav.userDetails(),
                                   banks=Getters.getBanks(), fad=Getters.getCustomerAccountDetails(acc_num))
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            return render_template('banking/deposits.html', record=record, user=Nav.userDetails(),
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
            TransactionUpdate.accChargeUpdate('RTGS', from_acc, Getters.getSysDate().date)
            flash('RTGS Successful')
            return redirect(url_for('banking.external_transfer'))
    else:
        record = []
        # fad = From Account Details
        # tad = To Account Details
        fad = None
        tad = None
        return render_template('banking/external_transfer.html', fad=fad, tad=tad, record=record,
                               user=Nav.userDetails(), banks=Getters.getBanks())


@banking.route('/with_account_search/', methods=['post', 'get'])
def with_account_search():
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            return render_template('banking/withdrawal.html', record=record, user=Nav.userDetails())
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            return render_template('banking/withdrawal.html', record=record, user=Nav.userDetails())
    else:
        return redirect(url_for('banking.withdrawal'))


@banking.route('/withdrawal', methods=['POST', 'GET'])
def withdrawal():
    record = None
    if request.method == 'POST':
        if Checker.userTillLink(login_session['username']):

            acc_num = int(request.form['client_account'])
            if Checker.accNumberChecker(acc_num):
                date = Getters.getSysDate().date  # time.strftime('%Y-%m-%d')
                dep_ref = request.form['withdrawal_ref']
                trantype = 'DR'
                ref = 'DR' + Auto.referenceStringGen()
                amount = float(request.form['withdrawal_amount'])

                TransactionUpdate.withdrawalTransactionUpdate(date, acc_num, amount, ref)
                TransactionUpdate.accChargeUpdate(trantype, acc_num, date)
                TransactionUpdate.ttUpdate('CR', amount, date, dep_ref, acc_num)
                flash('Account Debited')
                return redirect(url_for('banking.withdrawal', user=Nav.userDetails()))
            else:
                flash('Account Cannot be found: Search again')
                return redirect(url_for('banking.withdrawal', user=Nav.userDetails()))
        else:
            flash('User is not linked to Any Till. Please Open a Till First')
            return redirect(url_for('banking.withdrawal', user=Nav.userDetails()))
    else:
        return render_template('banking/withdrawal.html', record=record, user=Nav.userDetails())


        # End of banking views

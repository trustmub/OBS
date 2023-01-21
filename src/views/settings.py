import datetime

from flask import Blueprint, render_template, redirect, request, url_for, flash

from src import db
from src.functions.genarators import Getters, TransactionUpdate
from src.functions.user_profile import Profile
from src.models.account_type_model import AccountType
from src.models.bank_table_model import Banks
from src.models.branch_model import Branch
from src.models.transaction_charge_fee_model import TransactionChargeFee

settings = Blueprint('settings', __name__)


@settings.route('/add_tran_type/', methods=['POST', 'GET'])
def add_tran_type():
    if request.method == 'POST':
        tran_type = str.upper(request.form['tran_type'])
        tran_charge = float(request.form['tran_charge'])
        new = TransactionChargeFee(tran_type=tran_type,
                                   tran_charge=tran_charge)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_trans_type.html', user=Profile().user_details())


@settings.route('/del_tran_type/<int:tid>/')
def del_tran_type(tid):
    trans_id = int(tid)

    record = db.session.query(TransactionChargeFee).filter_by(id=trans_id).first()
    db.session.delete(record)
    db.session.commit()
    flash('Transaction Type Record Deleted')
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_acc_type/', methods=['POST', 'GET'])
def add_acc_type():
    if request.method == 'POST':
        acc_type = str.capitalize(request.form['acc_type'])
        min_balance = int(request.form['min_balance'])
        new = AccountType(acc_type=acc_type,
                          minbalance=min_balance)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_acc_type.html', user=Profile().user_details())


@settings.route('/del_acc_type/<int:id>/')
def del_acc_type(id):
    tid = id
    record = db.session.query(AccountType).filter_by(id=tid).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_branch/', methods=['POST', 'GET'])
def add_branch():
    if request.method == 'POST':
        code = request.form['branch_code']
        description = request.form['description']
        date = datetime.datetime.now()
        new = Branch(code=code,
                     description=description,)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('settings.system_setting'))
        pass
    else:
        return render_template('settings/add_branch.html', user=Profile().user_details())


@settings.route('/del_branch/<int:id>/', methods=['POST', 'GET'])
def del_branch(id):
    record = db.session.query(Branch).filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_bank/', methods=['POST', 'GET'])
def add_bank():
    if request.method == 'POST':
        name = request.form['name']
        swift_code = str.upper(request.form['swift_code'])
        new = Banks(name=name,
                    swift_code=swift_code)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_bank.html', user=Profile().user_details())


@settings.route('/delete_bank/<int:id>/', methods=['POST', 'GET'])
def delete_bank(id):
    record = db.session.query(Banks).filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('settings.system_setting'))


@settings.route('/system_setting/')
def system_setting():
    return render_template('settings/system_settings.html', user=Profile().user_details(),
                           tran=TransactionUpdate.getTransationTypeCharge(), acct=Getters.getAccountType(),
                           branch=Getters.getBranch(), banks=Getters.getBanks(), currency=Getters.getCurrency())


@settings.route('/user_setting/')
def user_setting():
    return render_template('settings/user_settings.html', user=Profile().user_details())


@settings.route('/information_setting/')
def information_setting():
    return render_template('settings/information_settings.html', user=Profile().user_details())

from flask import Blueprint, render_template, redirect, request, url_for
from src.functions.genarators import *

settings = Blueprint('settings', __name__)


@settings.route('/add_tran_type/', methods=['POST', 'GET'])
def add_tran_type():
    if request.method == 'POST':
        tran_type = str.upper(request.form['tran_type'])
        tran_charge = float(request.form['tran_charge'])
        new = TransactionCharge(tran_type=tran_type,
                                tran_charge=tran_charge)
        session.add(new)
        session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_trans_type.html', user=Profile().user_details())


@settings.route('/del_tran_type/<int:tid>/')
def del_tran_type(tid):
    trans_id = int(tid)

    record = session.query(TransactionCharge).filter_by(id=trans_id).first()
    session.delete(record)
    session.commit()
    flash('Transaction Type Record Deleted')
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_acc_type/', methods=['POST', 'GET'])
def add_acc_type():
    if request.method == 'POST':
        acc_type = str.capitalize(request.form['acc_type'])
        min_balance = int(request.form['min_balance'])
        new = Account(acc_type=acc_type,
                      minbalance=min_balance)
        session.add(new)
        session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_acc_type.html', user=Profile().user_details())


@settings.route('/del_acc_type/<int:id>/')
def del_acc_type(id):
    tid = id
    record = session.query(Account).filter_by(id=tid).first()
    session.delete(record)
    session.commit()
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_branch/', methods=['POST', 'GET'])
def add_branch():
    if request.method == 'POST':
        code = request.form['branch_code']
        description = request.form['description']
        date = datetime.datetime.now()
        new = Branch(code=code,
                     description=description,)
        session.add(new)
        session.commit()
        return redirect(url_for('settings.system_setting'))
        pass
    else:
        return render_template('settings/add_branch.html', user=Profile().user_details())


@settings.route('/del_branch/<int:id>/', methods=['POST', 'GET'])
def del_branch(id):
    record = session.query(Branch).filter_by(id=id).first()
    session.delete(record)
    session.commit()
    return redirect(url_for('settings.system_setting'))


@settings.route('/add_bank/', methods=['POST', 'GET'])
def add_bank():
    if request.method == 'POST':
        name = request.form['name']
        swift_code = str.upper(request.form['swift_code'])
        new = Banks(name=name,
                    swift_code=swift_code)
        session.add(new)
        session.commit()
        return redirect(url_for('settings.system_setting'))
    else:
        return render_template('settings/add_bank.html', user=Profile().user_details())


@settings.route('/delete_bank/<int:id>/', methods=['POST', 'GET'])
def delete_bank(id):
    record = session.query(Banks).filter_by(id=id).first()
    session.delete(record)
    session.commit()
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

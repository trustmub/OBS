import datetime
import time

from flask import Blueprint, redirect, render_template, url_for, request

from functions.genarators import *
from models import Base, Customer, Transactions

reconciliation = Blueprint('reconciliation', __name__)

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@reconciliation.route('/teller_reversal/')
def reversal_teller():
    record = None
    if request.method == 'POST':
        pass
    else:
        return render_template('reconciliation/teller_reversal.html', record=record, user=Nav.userDetails())


@reconciliation.route('/recon_reverse_withdrawals/')
def reversal_withdrawal():
    record = None
    if request.method == 'POST':
        pass
    else:
        return render_template('reconciliation/withdrawal_reversal.html', record=record, user=Nav.userDetails())
    pass


@reconciliation.route('/transfer_reversal/')
def reversal_transfer():
    pass


@reconciliation.route('/servfee_reversal/')
def reversal_servfee():
    pass


@reconciliation.route('/interest_reversal')
def reversal_interest():
    pass


@reconciliation.route('/teller_transactions')
def teller_transactions():
    record = None
    return render_template('reconciliation/teller_transactions.html', my_tt=Getters.getAllTts(), record=record,
                           user=Nav.userDetails())

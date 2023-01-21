from flask import Blueprint, render_template, request

from src.functions.genarators import Getters
from src.functions.user_profile import Profile

reconciliation = Blueprint('reconciliation', __name__)


@reconciliation.route('/teller_reversal/')
def reversal_teller():
    record = None
    if request.method == 'POST':
        pass
    else:
        return render_template('reconciliation/teller_reversal.html', record=record, user=Profile().user_details())


@reconciliation.route('/recon_reverse_withdrawals/')
def reversal_withdrawal():
    record = None
    if request.method == 'POST':
        pass
    else:
        return render_template('reconciliation/withdrawal_reversal.html', record=record, user=Profile().user_details())
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
                           user=Profile().user_details())

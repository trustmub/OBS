from flask import Flask, render_template

from views.user import user
from views.banking import banking
from views.customer import customer
from views.till import till
from views.settings import settings
from views.recon import reconciliation
from functions.genarators import *

app = Flask(__name__)
app.secret_key = 'asdkerhg8927qr9w0rhgwe70gw9eprg7w0e9r7g'
app.register_blueprint(user)
app.register_blueprint(banking)
app.register_blueprint(customer)
app.register_blueprint(till)
app.register_blueprint(reconciliation)
app.register_blueprint(settings)


@app.route('/dashboard/')
def home():
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')

    usr = session.query(User).all()
    interest = session.query(Interest).all()
    return render_template('dashboard.html', usr=usr, user=Nav.userDetails(), teller=Getters.getTillDetails(),
                           withd=Getters.getTellerWithdrawal(), deposits=Getters.getTellerDeposits(), interest=interest,
                           sys_date=sys_date.strftime('%d %B %Y'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template

from functions.genarators import *

from views.user import user
from views.banking import banking
from views.customer import customer
from views.till import till
from views.settings import settings
from views.recon import reconciliation
from views.enquiry import enquiry
from views.bulk import bulk

app = Flask(__name__)
app.secret_key = 'asdkerhg8927qr9w0rhgwe70gw9eprg7w0e9r7g'
app.register_blueprint(user)
app.register_blueprint(banking)
app.register_blueprint(customer)
app.register_blueprint(till)
app.register_blueprint(reconciliation)
app.register_blueprint(enquiry)
app.register_blueprint(bulk)
app.register_blueprint(settings)


@app.route('/dashboard/')
def home():
    sys_date = datetime.datetime.strptime(Getters.getSysDate().date, '%Y-%m-%d')

    usr = session.query(User).all()
    # interest = session.query(Interest).all()
    return render_template('dashboard.html', usr=usr, user=Profile().user_details(), teller=Getters.getTillDetails(),
                           withd=Getters.getTellerWithdrawal(), deposits=Getters.getTellerDeposits(),
                           sys_date=sys_date.strftime('%d %B %Y'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)

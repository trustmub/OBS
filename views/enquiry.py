from flask import Blueprint, render_template, redirect, request, url_for, flash

from functions.genarators import *
from models import Base, Customer, Transactions

enquiry = Blueprint('enquiry', __name__)

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@enquiry.route('/account_reset')
def account_reset():
    record = []
    return render_template('enquiry/account_reset.html', record=record, user=Nav.userDetails())

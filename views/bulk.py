from flask import Blueprint, render_template, redirect, request, url_for, flash

from functions.genarators import *
from models import Base, Customer, Transactions

bulk = Blueprint('bulk', __name__)

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@bulk.route('/bulk_salaries')
def bulk_salaries():
    record = []
    return render_template('bulk/bulk_salaries.html', record=record, user=Nav.userDetails())

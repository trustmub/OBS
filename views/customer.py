import time
import datetime

from flask import Blueprint, render_template, redirect, request, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functions.genarators import *
from functions.transactions import AccountTransaction
from models import Base, Customer

customer = Blueprint('customer', __name__)

engine = create_engine('sqlite:///bnk.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@customer.route('/add_cus/', methods=['POST', 'GET'])
def add_cus():
    new_account = Auto.accountNumGen()
    # name = request.form['first_name']

    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        country = request.form['country']
        acc_number = request.form['acc_number']
        working_bal = float(request.form['working_bal'])
        account_type = request.form['account_type']

        new = Customer(first_name=first_name,
                       last_name=last_name,
                       dob=dob,
                       gender=gender,
                       contact_number=contact_number,
                       email=email,
                       address=address,
                       country=country,
                       acc_number=new_account,
                       working_bal=working_bal,
                       account_type=account_type,
                       create_date=datetime.datetime.now(),
                       inputter_id=Nav.userDetails().uid)
        session.add(new)
        session.commit()
        # TransactionUpdate.accCreationCash(time.strftime('%Y-%m-%d'), working_bal, new_account)

        AccountTransaction(time.strftime('%Y-%m-%d'), working_bal, new_account).create_account()

        return redirect(url_for('customer.my_cus'))
    else:
        return render_template('customer/add_cus.html', new_account=new_account, user=Nav.userDetails(),
                               account=Getters.getAccountType())


@customer.route('/id_search/', methods=['post', 'get'])
def id_search():
    if request.method == 'POST':
        id_num = int(request.form['customer_id'])
        if session.query(Customer).filter_by(custid=id_num).first():
            record = session.query(Customer).filter_by(custid=id_num).first()
            return render_template('customer/amend_cus.html', record=record, user=Nav.userDetails(),
                                   account=Getters.getAccountType())
        else:
            flash('The Customer System ID Provided Is NOT Valid')
            record = None
            return render_template('customer/amend_cus.html', record=record, user=Nav.userDetails())
    else:
        flash('Failed to go through the IF STMT')
        return redirect(url_for('customer.amend_cus', user=Nav.userDetails()))


@customer.route('/cus_account_search/', methods=['post', 'get'])
def account_search():
    if request.method == 'POST':
        acc_num = int(request.form['account_number'])
        if session.query(Customer).filter_by(acc_number=acc_num).first():
            record = session.query(Customer).filter_by(acc_number=acc_num).first()
            return render_template('customer/amend_cus.html', record=record, user=Nav.userDetails(),
                                   account=Getters.getAccountType())
        else:
            flash('The Account Number Provided Is NOT In The System')
            record = None
            return render_template('customer/amend_cus.html', record=record, user=Nav.userDetails())
    else:
        return redirect(url_for('customer.amend_cus', user=Nav.userDetails()))


@customer.route('/amend_cus/', methods=['POST', 'GET'])
def amend_cus():
    record = None
    if request.method == 'POST':
        acc_num = int(request.form['acc_number'])
        if Checker.accNumberChecker(acc_num):

            a_record = session.query(Customer).filter_by(acc_number=acc_num).one()
            if request.form['first_name'] == a_record.first_name:
                pass
            else:
                a_record.first_name = request.form['first_name']
            if request.form['last_name'] == a_record.last_name:
                pass
            else:
                a_record.last_name = request.form['last_name']
            if request.form['dob'] == a_record.dob:
                pass
            else:
                a_record.dob = request.form['dob']
            if request.form['gender'] == a_record.gender:
                pass
            else:
                a_record.gender = request.form['gender']
            if request.form['contact_number'] == a_record.contact_number:
                pass
            else:
                a_record.contact_number = int(request.form['contact_number'])
            if request.form['email'] == a_record.email:
                pass
            else:
                a_record.email = request.form['email']
            if request.form['address'] == a_record.address:
                pass
            else:
                a_record.address = request.form['address']
            if request.form['country'] == a_record.country:
                pass
            else:
                a_record.country = request.form['country']
            '''if request.form['acc_number'] == a_record.acc_number:
                pass
            else:
                a_record.acc_number = request.form['acc_number']
            if request.form['working_bal'] == a_record.working_bal:
                pass
            else:
                a_record.working_bal = float(request.form['working_bal'])'''
            if request.form['account_type'] == a_record.account_type:
                pass
            else:
                a_record.account_type = request.form['account_type']
            a_record.create_date = a_record.create_date

            session.add(a_record)
            session.commit()
            return redirect(url_for('customer.my_cus', user=Nav.userDetails()))
        else:
            flash('Account Cannot be modified, Search Again')
            record = None
            return redirect(url_for('customer.amend_cus'))
    else:
        return render_template('customer/amend_cus.html', record=record, user=Nav.userDetails(),
                               account=Getters.getAccountType())


@customer.route('/authorise/')
def authorise_cus():
    return render_template('customer/authorise.html', user=Nav.userDetails())


@customer.route('/my_cus/')
def my_cus():
    all_customer = session.query(Customer).all()
    return render_template('customer/my_cus.html', customer=all_customer, user=Nav.userDetails())

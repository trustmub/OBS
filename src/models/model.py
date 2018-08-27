from datetime import datetime
from . import APP
from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(APP)


class Customer(db.Model):
    id = db.column(db.Integer, primary_key=True)
    first_name = db.column(db.String(50))
    middle_name = db.column(db.String(50))
    surname = db.column(db.String(50))

    address_id = db.column(db.Integer, db.ForeignKey('address.id'))

    gender = db.column(db.String(20))
    business_phone = db.column(db.Integer)
    home_phone = db.column(db.Integer)
    cell_phone = db.column(db.Integer)

    nationality_id = db.column(db.Integer, db.ForeignKey('country.id'))  # get from Country table
    national_type_id = db.column(db.Integer, db.ForeignKey('identification.id'))  # get from the identification table
    identification_number = db.column(db.String(20))
    race_id = db.column(db.Integer, db.ForeignKey('race.id'))  # get from race table
    religion_id = db.column(db.Integer, db.ForeignKey('religion.id'))  # get from religion table

    flagged_for_closure = db.column(db.Boolean, default=False)
    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)


class Address(db.Model):
    id = db.column(db.Integer, primary_key=True)
    street = db.column(db.String(100))
    city = db.column(db.String(100))
    province = db.column(db.String(100))
    postal_zip = db.column(db.String(20))
    customer = db.relationship('Customer', backref='address', uselist=False, lazy='dynamic')

    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)


class Country(db.Model):
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(100))
    country_code = db.column(db.String(20))

    customer = db.relationship('Customer', backref='country', uselist=False, lazy='dynamic')

    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)


class Identification(db.Model):
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(50))
    code = db.column(db.String(20))

    customer = db.relationship('Customer', backref='identification', uselist=False, lazy='dynamic')

    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)


class Race(db.Model):
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(50))
    code = db.column(db.String(20))

    customer = db.relationship('Customer', backref='race', uselist=False, lazy='dynamic')

    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)


class Religion(db.Model):
    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(50))
    code = db.column(db.String(20))

    customer = db.relationship('Customer', backref='religion', uselist=False, lazy='dynamic')

    amend_by = db.column(db.String(30))
    created_by = db.column(db.String(30))
    amend_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)
    create_date = db.column(db.DateTime, nullable=False, default=datetime.utcnow)

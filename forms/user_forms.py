from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationsForm(FlaskForm):
    fullname = StringField('Username', validators=[DataRequired(), Length(min=4)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    ts_and_cs = BooleanField('Agree to ')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    remember_me = BooleanField('Remeber me')
    submit = SubmitField('Login')


class UserProfile(FlaskForm):
    fullname = StringField('Username', validators=[DataRequired(), Length(min=4)])
    job_title = StringField('Job_Title')
    department = StringField('Department')
    branch_code = StringField('Branch_Code', validators=[DataRequired()])
    access_level = IntegerField('access_level', validators=[DataRequired()])
    image_string = StringField('image_string')
    submit = SubmitField('update')

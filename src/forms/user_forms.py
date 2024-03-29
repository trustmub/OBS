"""
    forms.user_forms
    ----------------

    forms for user input fields verifications and validation etc

"""

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from src import db
from src.forms import (FlaskForm, StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField,
                       FileField, FileAllowed)
from src.models.system_user_model import SystemUser


# from src.models.models import User


class RegistrationsForm(FlaskForm):
    """
    form class for user registrations
    """
    fullname = StringField('Username', validators=[DataRequired(), Length(min=4)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    ts_and_cs = BooleanField('Agree to ')
    submit = SubmitField('Register')

    def validate_email(self, email):
        """
        This method evaluates on submission if the user with the same email exists. if so a
        validation error is sent.
        :param email:
        :return: ValidationError
        """
        user = db.session.query(SystemUser).filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already exists. Please try a different one.")


class LoginForm(FlaskForm):
    """
    form class for user login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class LockScreenForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Login')


class UserProfileForm(FlaskForm):
    """
    form class for user profile edit.
    """
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=4)])
    job_title = StringField('Job Title')
    department = StringField('Department')
    branch_code = SelectField('Branch Code', validators=[DataRequired()])
    access_level = IntegerField('Access level', validators=[DataRequired()])
    image_string = FileField('Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

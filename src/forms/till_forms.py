from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.forms import (FlaskForm, SelectField, DecimalField, SubmitField, IntegerField)


class OpenTillForm(FlaskForm):
    """
    form class for till opening
    """
    branch = SelectField("Branch")
    teller_num = SelectField("Teller num")
    o_balance = DecimalField("Opening Balance", places=2)
    user_id = IntegerField("User ID")
    submit = SubmitField("Open Till")

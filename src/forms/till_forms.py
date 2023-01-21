from wtforms.validators import DataRequired
from src.forms import (FlaskForm, SelectField, DecimalField, SubmitField, IntegerField)


class OpenTillForm(FlaskForm):
    """
    form class for till opening
    """
    branch = SelectField("Branch", validators=[DataRequired()])
    teller_num = SelectField("Teller", validators=[DataRequired()])
    o_balance = DecimalField("Opening Balance", places=2, validators=[DataRequired()])
    user_id = IntegerField("User ID", validators=[DataRequired()])
    submit = SubmitField("Open Till")


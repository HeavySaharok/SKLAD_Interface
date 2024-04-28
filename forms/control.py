from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ControlForm(FlaskForm):
    output = StringField('Откуда', validators=[DataRequired()])
    input = StringField('Куда', validators=[DataRequired()])
    id_item = IntegerField("ID Товара", validators=[DataRequired()])
    count = IntegerField("Колличество", validators=[DataRequired()])
    submit = SubmitField('Отправить')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class WarehouseForm(FlaskForm):
    wh_name = StringField('Назввание склада', validators=[DataRequired()])
    coords = TextAreaField("Координаты")
    limit = IntegerField("Лимит вместимости")
    submit = SubmitField('Создать')

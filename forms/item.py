from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    item_name = StringField('Название предмета', validators=[DataRequired()])
    category = TextAreaField("Категория")
    amount = IntegerField("Колличество")
    collaborators = TextAreaField("Коллабораторы")
    is_finished = BooleanField("Работа завершена?")
    submit = SubmitField('Применить')

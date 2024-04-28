from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    item_name = StringField('Название предмета', validators=[DataRequired()])
    category = TextAreaField("Категория")
    price = IntegerField("Цена")
    weight = IntegerField("Вес")
    desc = TextAreaField("Описание (опционально)")
    submit = SubmitField('Создать предмет')

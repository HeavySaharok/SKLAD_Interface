from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class WarehouseForm(FlaskForm):
    """
    Форма для создания и редактирования склада
    """
    wh_name = StringField('Назввание склада', validators=[DataRequired()])
    coords = TextAreaField("Координаты")
    limit = IntegerField("Лимит вместимости")
    fullness = IntegerField("Текущая заполненность склада (опционально)")
    description = TextAreaField("Описание (опционально)")
    submit = SubmitField('Создать')

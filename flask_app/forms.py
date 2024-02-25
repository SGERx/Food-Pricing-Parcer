from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    """Форма добавления продукта для парсинга"""
    product = StringField("Наименование продукта", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

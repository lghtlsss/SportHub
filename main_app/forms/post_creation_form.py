from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField


class PostCreation(FlaskForm):
    title = StringField('Заголовок поста', validators=[DataRequired()])
    text = StringField('Текст поста', validators=[DataRequired()])
    contents = StringField('Вложения **пока не работает**')
    topic = StringField('Тема(не обязательно)')
    submit = SubmitField('Опубликовать')

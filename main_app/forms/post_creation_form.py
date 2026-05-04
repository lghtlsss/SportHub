from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField, FileField, TextAreaField
from flask_wtf.file import FileAllowed


class PostCreation(FlaskForm):
    title = StringField('Заголовок поста', validators=[DataRequired()])
    text = TextAreaField('Текст поста', validators=[DataRequired()])
    contents = FileField('Прикрепите фотографию',
                         validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения (.jpg, .png, .jpeg)!')])
    topic = StringField('Вид спорта(не обязательно)')
    submit = SubmitField('Опубликовать')

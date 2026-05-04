from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, EmailField, SelectMultipleField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    email = EmailField('Введите вашу почту', validators=[DataRequired()])
    avatar = FileField('Прикрепите аватар(По желанию)',
                       validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения (.jpg, .png, .jpeg)!')])
    name = StringField('Введите ваше имя', validators=[DataRequired()])
    surname = StringField('Введите вашу фамилию', validators=[DataRequired()])
    age = IntegerField('Введите ваш возраст', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    description = StringField('О себе(По желанию)')
    pref_sport = SelectMultipleField('Выберите ваш спорт', validators=[DataRequired()],
                                     choices=[(1, 'Бег'), (2, 'Велоспорт'), (3, 'Тяжелая атлетика'),
                                              (4, 'Фитнес/Похудение')])
    submit = SubmitField('Зарегистрироваться')

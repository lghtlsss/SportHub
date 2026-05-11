from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SelectMultipleField, SubmitField, FileField
from wtforms.validators import DataRequired, InputRequired


class EdbtProfileForm(FlaskForm):
    name = StringField('Введите ваше имя', validators=[DataRequired()])
    surname = StringField('Введите вашу фамилию', validators=[DataRequired()])
    age = IntegerField('Введите ваш возраст', validators=[DataRequired()])
    description = StringField('О себе(По желанию)')
    pref_sport = SelectMultipleField('Выберите ваш спорт', validators=[InputRequired()],
                                     choices=[('Бег', 'Бег'), ('Велоспорт', 'Велоспорт'),
                                              ('Тяжелая атлетика', 'Тяжелая атлетика'),
                                              ('Фитнес/Похудение', 'Фитнес/Похудение')])
    submit = SubmitField('Изменить')

from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
from wtforms import PasswordField, EmailField, SubmitField, BooleanField


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти', validators=[DataRequired()])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


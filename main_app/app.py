import sqlalchemy
from flask import Flask, render_template, request, redirect
from flask_login import login_required, logout_user, current_user, LoginManager, login_user

from data.user import User
from forms.__all_forms import *
from data import db_session
from data.__all_models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='Главная')


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        session = db_session.create_session()
        user = session.query(User).get(current_user.id)
        return render_template("profile.html", name=user.name, title='Профиль')
    return render_template("profile.html", title='Профиль')


@app.route('/subscriptions')
def subscriptions():
    return ''


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if not session.query(User).filter(User.email == form.email.data).first():
            if form.password.data == form.password_again.data:
                new_user = User(
                    email=form.email.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    age=form.age.data,
                    description=form.description.data,
                    pref_sport=",".join(form.pref_sport.data)
                )
                new_user.set_password(form.password.data)
                session.add(new_user)
                session.commit()
                return redirect("/profile")
            return render_template("register.html", form=form, message='Пароли не совпадают')
        return render_template("register.html", form=form,message='Адрес электронной почты занят')
    return render_template("register.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        possible_user = session.query(User).filter(User.email == form.email.data).first()
        if possible_user and possible_user.check_password(form.password.data):
            login_user(possible_user, remember=form.remember_me.data)
            return redirect('/profile')
        return render_template('login.html', title='Аторизация', message='Неверный пароль', form=form)
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


def main():
    db_session.global_init('../db/base_2.db')
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()

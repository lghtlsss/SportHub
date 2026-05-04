from flask import render_template, redirect, request
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_restful import Api

from app_dir.app_class import app
from forms.__all_forms import *
from data import db_session
from data.__all_models import *
from resources.post_resource import PostResource, PostListResource
from resources.user_resourse import UserResource, ListUserResource

login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(PostResource, '/api/post/<int:post_id>')
api.add_resource(PostListResource, '/api/posts')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(ListUserResource, '/api/users')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='Главная')


# TODO: Сделать без подзагрузок с js + api
@app.route("/posts_line")
def posts_line():
    session = db_session.create_session()
    first_20 = session.query(Post).limit(20).all()
    return render_template("posts_line.html", title='Лента', posts=first_20)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        session = db_session.create_session()
        user = session.query(User).get(current_user.id)
        return render_template("profile.html", name=user.name, surname=user.surname, age=user.age,
                               sport=user.pref_sport, title='Профиль')
    return render_template("profile.html", title='Профиль')


@app.route('/subscriptions')
def subscriptions():
    session = db_session.create_session()
    user = session.get(User, current_user.id)
    subs = session.query(Subscriber).filter(Subscriber.subscriber_user_id == user.id).all()
    return render_template('subscriptions.html', title='Подписки',
                           subs=[[item.user.name, item.user.surname] for item in subs])


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
        return render_template("register.html", form=form, message='Адрес электронной почты занят')
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
@login_required
def logout():
    logout_user()
    return redirect('/')


# TODO: Переделать через api + js?
@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostCreation()
    if form.validate_on_submit():
        session = db_session.create_session()
        author = session.query(User).get(current_user.id)
        new_post = Post(title=form.title.data,
                        author=f'{author.name} {author.surname}',
                        text=form.text.data,
                        contents=form.contents.data,
                        topic=form.topic.data
                        )
        session.add(new_post)
        session.commit()
        return redirect('/posts_line')
    return render_template('post_creation.html', title='Публикация поста', form=form)


# TODO: Просмотр поста
@app.route('/view_post/<int:post_id>')
def view_post():
    pass


def main():
    db_session.global_init('../db/base_11.db')
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()

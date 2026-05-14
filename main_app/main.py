from flask import render_template, redirect, request
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_restful import Api, abort

from app_dir.app_class import app
from main_app.forms.__all_forms import *
from main_app.tools import time_tool, image_request_tool
from data import db_session
from data.__all_models import *
from resources.post_resource import PostResource, PostListResource
from resources.user_resourse import UserResource, ListUserResource
from resources.avatar_resource import AvatarResource
from resources.comment_resource import CommentListResource, CommentResource
from resources.image_resource import ImageResource
from resources.feed_resource import FeedResource

from PIL import Image as Im
import io

# TODO: flask-limiter

login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(PostResource, '/api/post/<int:post_id>')
api.add_resource(PostListResource, '/api/posts')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(ListUserResource, '/api/users')
api.add_resource(AvatarResource, '/api/avatar/<int:user_id>')
api.add_resource(CommentResource, '/api/user_comments')
api.add_resource(CommentListResource, '/api/post_comments')
api.add_resource(ImageResource, '/api/images/<int:post_id>')
api.add_resource(FeedResource, '/api/feed')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title='Главная')


@app.route("/posts_line")
@login_required
def posts_line():
    session = db_session.create_session()
    first_5 = session.query(Post).order_by(Post.id.desc()).limit(5).all()
    posts = [[item, time_tool.get_delta(item.creation_time), len(item.likes), image_request_tool.check_image(item.id)]
             for item in first_5]
    return render_template("posts_line.html", title='Лента', posts=posts, page_title='Лента')


@app.route('/view_post/<int:post_id>', methods=['POST', 'GET'])
def view_post(post_id):
    session = db_session.create_session()
    post = session.get(Post, post_id)
    try:
        if post:
            if request.method == 'POST':
                comment_text = request.form.get('comment')
                new_comment = Comment(
                    post_id=post_id,
                    author_id=current_user.id,
                    content=comment_text
                )
                session.add(new_comment)
                session.commit()
            str_delta = time_tool.get_delta(post.creation_time)
            likes_count = len(post.likes)
            is_image = image_request_tool.check_image(post_id)
            user = session.get(User, post.author_id)
            is_subscribed = current_user.id in [sub.subscriber_user_id for sub in user.subscribers]
            return render_template('view_post.html', title='Просмотр поста', post=post, delta=str_delta,
                                   likes_count=likes_count, is_image=is_image, is_subscribed=is_subscribed)
        return redirect("/posts_line")
    finally:
        session.close()


@app.route('/profile')
@login_required
def profile():
    session = db_session.create_session()
    user = session.get(User, current_user.id)
    return render_template("profile.html", name=user.name, surname=user.surname, age=user.age,
                           sport=user.pref_sport, about=user.description, title='Профиль')


@app.route('/profile/delete/<int:user_id>')
@login_required
def delete_profile(user_id):
    session = db_session.create_session()
    user = session.get(User, user_id)
    if user:
        logout_user()
        session.delete(user)
        session.commit()
        return redirect('/register')
    return abort(404)


@app.route('/profile/edit/<int:user_id>', methods=["POST", "GET"])
@login_required
def profile_edit(user_id):
    form = EdbtProfileForm()
    session = db_session.create_session()
    user = session.get(User, user_id)
    if user:
        if request.method == 'GET':
            form.name.data = user.name
            form.surname.data = user.surname
            form.age.data = user.age
            form.description.data = user.description
            form.pref_sport.data = user.pref_sport
            return render_template('profile_edit.html', form=form)
        if form.validate_on_submit():
            if form.name.data:
                user.name = form.name.data
            if form.surname.data:
                user.surname = form.surname.data
            if form.age.data:
                user.age = form.age.data
            if form.description.data:
                user.description = form.description.data
            if form.pref_sport.data:
                user.pref_sport = ", ".join(form.pref_sport.data)
            session.commit()
            session.close()
            return redirect('/profile')

    return abort(404, message='User not found')


@app.route('/my_posts')
@login_required
def my_posts():
    session = db_session.create_session()
    try:
        posts = [
            [item, time_tool.get_delta(item.creation_time), len(item.likes), image_request_tool.check_image(item.id)]
            for item in session.query(Post).filter(Post.author_id == current_user.id).all()]
        return render_template("posts_line.html", page_title='Ваши посты', title='Лента', posts=posts)
    finally:
        session.close()


@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='О нас')


@app.route('/subscriptions')
@login_required
def subscriptions():
    session = db_session.create_session()
    subs = session.query(Subscriber).filter(Subscriber.subscriber_user_id == current_user.id).all()
    return render_template('subscriptions.html', title='Подписки',
                           subs=[[item.id, item.user.name, item.user.surname] for item in subs])


@app.route('/subscribers')
@login_required
def subscribers():
    session = db_session.create_session()
    subs = session.get(User, current_user.id).subscribers
    if subs:
        subs_users = [session.get(User, sub.subscriber_user_id) for sub in subs]
        session.close()
        return render_template('subscribers.html', subs=subs_users, is_any_subs=True)
    session.close()
    return render_template('subscribers.html', is_any_subs=False)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if not session.query(User).filter(User.email == form.email.data).first():
            if form.password.data == form.password_again.data:
                file = form.avatar.data
                if file:
                    img = Im.open(file)
                    img.thumbnail((256, 256))
                    img = img.convert("RGB")
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=95)
                    avatar = Avatar(
                        content=buffer.getvalue(),
                        mime="image/jpeg"
                    )
                else:
                    with open('main_app/static/images/no_avatar.jpg', 'rb') as no_avatar_f:
                        avatar = Avatar(
                            content=no_avatar_f.read(),
                            mime='image/jpg'
                        )
                session.add(avatar)
                session.flush()
                new_user = User(
                    email=form.email.data,
                    avatar=avatar,
                    name=form.name.data,
                    surname=form.surname.data,
                    age=form.age.data,
                    description=form.description.data,
                    pref_sport=", ".join(form.pref_sport.data)
                )
                new_user.set_password(form.password.data)
                session.add(new_user)
                session.commit()
                return redirect("/login")
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
        return render_template('login.html', title='Авторизация', message='Неверный пароль', form=form)
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostCreation()
    if form.validate_on_submit():
        session = db_session.create_session()
        author = session.get(User, current_user.id)
        file = form.contents.data
        if file:
            img = Im.open(file)
            img.thumbnail((1920, 1080))
            img = img.convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            image = Image(
                content=buffer.getvalue(),
                mime="image/jpeg"
            )
            session.add(image)
            session.flush()
            new_post = Post(title=form.title.data,
                            author=f'{author.name} {author.surname}',
                            author_id=current_user.id,
                            text=form.text.data,
                            topic=form.topic.data,
                            image=image
                            )
        else:
            new_post = Post(title=form.title.data,
                            author=f'{author.name} {author.surname}',
                            author_id=current_user.id,
                            text=form.text.data,
                            topic=form.topic.data,
                            )
        session.add(new_post)
        session.commit()
        return redirect('/success')
    return render_template('post_creation.html', title='Публикация поста', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


def main():
    db_session.global_init('db/SportHubBase.db')
    app.run(port=8070, host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()

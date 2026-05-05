from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data.like import Like
from data.post import Post
from data import db_session
from data.user import User


def abort_if_not_found(session, thing_id):
    thing = session.query(Post).get(thing_id)
    if not thing:
        abort(404, message='Post not found')


parser = reqparse.RequestParser()
parser.add_argument('likes', location='json', required=True)
parser.add_argument('user', location='json', required=True)


class PostResource(Resource):
    def get(self, post_id):
        session = db_session.create_session()
        try:
            post = session.get(Post, post_id)
            return jsonify({'post': post})
        except Exception as e:
            return {'error': str(e)}, 500

    def delete(self, post_id):
        session = db_session.create_session()
        abort_if_not_found(session, post_id)
        post = session.query(Post).get(post_id)
        session.delete(post)
        session.commit()
        return jsonify({'message': 'success'})

    def patch(self, post_id):
        session = db_session.create_session()
        abort_if_not_found(session, post_id)
        args = parser.parse_args()
        user = session.get(User, args['user'])
        like = session.query(Like).filter_by(
            user_id=user.id,
            post_id=post_id
        ).first()
        if like:
            session.delete(like)
        else:
            session.add(Like(user_id=user.id, post_id=post_id))
        session.commit()
        likes_count = session.query(Like).filter_by(post_id=post_id).count()

        return {'likes': likes_count}

    def to_dict(self, post):
        return {
            'id': post.id,
            'title': post.title,
            'likes': [like.id for like in post.likes]  # только id
        }


list_parser = reqparse.RequestParser()
list_parser.add_argument('author', required=True)
list_parser.add_argument('text', required=True)
list_parser.add_argument('contents',
                         required=True)  # вот тут мб что-то с типами сделать, тк в контенте должна быть картинка, но скорее всего буду хранить в последовательности байт
list_parser.add_argument('topic', required=True)


class PostListResource(Resource):
    def get(self):
        session = db_session.create_session()
        posts = session.query(Post).all()
        if not posts:
            abort(404, message='Not found')
        return jsonify({'posts': [item.to_dict(only=['id', 'author', 'title', 'text', 'topic']) for item in posts]})

    def post(self):
        args = list_parser.parse_args()
        session = db_session.create_session()
        new_post = Post(
            author=args['author'],
            text=args['text'],
            contents=args['contents'],
            topic=args['topic']
        )
        session.add(new_post)
        session.commit()
        return jsonify({'id': new_post.id})

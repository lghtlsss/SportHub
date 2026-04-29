from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data.post import Post
from data import db_session


def abort_if_not_found(session, thing_id):
    thing = session.query(Post).get(thing_id)
    if not thing:
        abort(404, message='Post not found')


class PostResource(Resource):
    def get(self, post_id):
        session = db_session.create_session()
        abort_if_not_found(session, post_id)
        post = session.query(Post).get(post_id)
        return jsonify({'post': post.to_dict()})

    def delete(self, post_id):
        session = db_session.create_session()
        abort_if_not_found(session, post_id)
        post = session.query(Post).get(post_id)
        session.delete(post)
        session.commit()
        return jsonify({'message': 'success'})


parser = reqparse.RequestParser()
parser.add_argument('author', required=True)
parser.add_argument('text', required=True)
parser.add_argument('contents',
                    required=True)  # вот тут мб что-то с типами сделать, тк в контенте должна быть картинка, но скорее всего буду хранить в последовательности байт
parser.add_argument('topic', required=True)


class PostListResource(Resource):
    def get(self):
        session = db_session.create_session()
        posts = session.query(Post).all()
        if not posts:
            abort(404, message='Not found')
        return jsonify({'posts': [item.to_dict() for item in posts]})

    def post(self):
        args = parser.parse_args()
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

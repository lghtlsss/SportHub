from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data.db_session import create_session
from data.__all_models import Comment


def abort_if_not_found(session, thing_id, thing_class):
    thing = session.get(thing_class, thing_id)
    if not thing:
        return abort(404, message='Comment not found')
    return None


parser = reqparse.RequestParser()
parser.add_argument('user_id', location='json', required=True)
parser.add_argument('post_id', location='json', required=True)


class CommentResource(Resource):
    def get(self):
        """Возвращает json комментариев пользователя под определённым постом"""
        session = create_session()
        args = parser.parse_args()
        post_id, user_id = args['post_id'], args['user_id']
        comments = session.query(Comment).filter_by(post_id=post_id, author_id=user_id).all()
        return jsonify({'comments': [item.to_dict(only=['id', 'post_id', 'author_id', 'content', 'creation_time']) for
                                     item in comments]})

    def to_dict(self, item):
        return {
            'post_id': item.post_id,
            'user_id': item.user_id,
            'text': item.content
        }


list_parser = reqparse.RequestParser()
list_parser.add_argument('post_id', location='json', required=True)


class CommentListResource(Resource):
    def get(self):
        """Возвращает json всех комментариев по id поста из list_parser"""
        session = create_session()
        comments = session.query(Comment).all()
        if not comments:
            return abort(404, message='Not found')
        return jsonify({'comments': [item.to_dict(only=['id', 'post_id', 'author_id', 'content', 'creation_time']) for item in comments]})

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
parser.add_argument('content', location='json')


class CommentResource(Resource):
    def get(self):
        """Возвращает json комментариев пользователя под определённым постом"""
        session = create_session()
        try:
            args = parser.parse_args()
            post_id, user_id = args['post_id'], args['user_id']
            comments = session.query(Comment).filter_by(post_id=post_id, author_id=user_id).all()
            return jsonify({'comments': [item.to_dict(only=['id', 'post_id', 'author_id', 'content', 'creation_time']) for
                                         item in comments]})
        finally:
            session.close()

    def post(self):
        session = create_session()
        try:
            args = parser.parse_args()
            post_id, user_id = args['post_id'], args['user_id']
            text = args['content']
            if not text:
                return abort(404, message='Empty content')
            comment = Comment(
                post_id=post_id,
                author_id=user_id,
                content=text
            )
            session.add(comment)
            session.commit()
            return jsonify({'message': 'success', 'comm_id': comment.id})
        finally:
            session.close()


list_parser = reqparse.RequestParser()
list_parser.add_argument('post_id', location='json', required=True)


class CommentListResource(Resource):
    def get(self):
        """Возвращает json всех комментариев по id поста из list_parser"""
        session = create_session()
        try:
            comments = session.query(Comment).all()
            if not comments:
                return abort(404, message='Not found')
            return jsonify({'comments': [item.to_dict(only=['id', 'post_id', 'author_id', 'content', 'creation_time']) for
                                         item in comments]})
        finally:
            session.close()

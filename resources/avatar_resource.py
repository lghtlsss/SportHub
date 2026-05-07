from flask import jsonify, Response
from flask_restful import Resource, abort

from data import avatar
from data.__all_models import Avatar, User
from data.db_session import create_session


def abort_if_not_found(session, thing_id, thing_class):
    thing = session.get(thing_class, thing_id)
    if not thing:
        abort(404, message='Not found')


class AvatarResource(Resource):
    def get(self, user_id):
        session = create_session()
        abort_if_not_found(session, user_id, User)
        user = session.get(User, user_id)
        avatar = user.avatar
        return Response(avatar.content, mimetype=avatar.mime)

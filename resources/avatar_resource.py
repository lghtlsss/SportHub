from flask import jsonify, Response
from flask_restful import Resource, abort

from data.avatar import Avatar
from data.db_session import create_session


def abort_if_not_found(session, thing_id):
    thing = session.get(Avatar, thing_id)
    if not thing:
        abort(404, message='Not found')


class AvatarResource(Resource):
    def get(self, avatar_id):
        session = create_session()
        abort_if_not_found(session, avatar_id)
        avatar = session.get(Avatar, avatar_id)
        return Response(avatar.content, mimetype=avatar.mime)


from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data.user import User
from data import db_session


class UserResource(Resource):
    def delete(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(session, user_id)
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'message': 'success'})

    def abort_if_user_not_found(self, session, us_id):
        res = session.query(User).get(us_id)
        if not res:
            abort(404, message='User not found')

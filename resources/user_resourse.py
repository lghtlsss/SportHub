from flask import jsonify
from flask_restful import Resource, abort, reqparse

from data.subscriber import Subscriber
from data.user import User
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('subscription_user', required=True, location='json')


class UserResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(session, user_id)
        try:
            user = session.get(User, user_id)
            return jsonify(
                {"user": user.to_dict(only=['id', 'email', 'name', 'surname', 'age', 'description', 'pref_sport'])})
        finally:
            session.close()

    def delete(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(session, user_id)
        try:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
            return jsonify({'message': 'success'})
        finally:
            session.close()

    def patch(self, user_id):
        session = db_session.create_session()
        self.abort_if_user_not_found(session, user_id)
        try:
            user = session.get(User, user_id)
            args = parser.parse_args()
            sub = session.query(Subscriber).filter_by(user_id=args['subscription_user'],
                                                      subscriber_user_id=user.id).first()
            if sub:
                session.delete(sub)
                session.commit()
                return jsonify({'new_btn_text': 'Подписаться'})
            else:
                session.add(Subscriber(
                    user_id=args['subscription_user'],
                    subscriber_user_id=user.id
                ))
                session.commit()
                return jsonify({'new_btn_text': 'Отписаться'})
            # subscribers = session.query(Subscriber).filter(Subscriber.user_id == user.id)
            # return jsonify({'subs': [item.to_dict() for item in subscribers]})
        finally:
            session.close()

    def abort_if_user_not_found(self, session, us_id):
        res = session.get(User, us_id)
        if not res:
            session.close()
            abort(404, message='User not found')


class ListUserResource(Resource):
    def get(self):
        session = db_session.create_session()
        try:
            users = session.query(User).all()
            return jsonify({"users": [
                item.to_dict(only=['id', 'email', 'name', 'surname', 'age', 'description', 'pref_sport']) for item in
                users]})
        finally:
            session.close()

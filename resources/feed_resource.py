from flask_restful import Resource
from flask import request, jsonify
from data.__all_models import Post
from data import db_session


class FeedResource(Resource):
    def get(self):
        last_id = request.args.get("last_id", type=int)
        if last_id:
            last_id += 1
            session = db_session.create_session()
            posts = session.query(Post).filter(Post.id < last_id).order_by(Post.id.desc()).limit(20).all()
            return jsonify({"posts": [item.to_dict(only=['id', 'author', 'title', 'text', 'topic']) for item in posts], "last_id": last_id - 20})
        return jsonify({'message': 'No last id'})


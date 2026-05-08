from flask_restful import Resource
from flask import request, jsonify
from data.__all_models import Post
from data import db_session
from data.post import Post
from main_app.tools import time_tool


class FeedResource(Resource):
    def get(self):
        session = db_session.create_session()
        try:
            last_id = request.args.get("last_id", type=int)

            query = session.query(Post).order_by(Post.id.desc())

            if last_id:
                query = query.filter(Post.id < last_id)

            posts = query.limit(5).all()

            posts_json = []

            for post in posts:
                post_data = post.to_dict(
                    only=['id', 'author', 'title', 'text', 'topic']
                )

                post_data["likes"] = len(post.likes)
                post_data["delta"] = time_tool.get_delta(post.creation_time)

                posts_json.append(post_data)

            return jsonify({
                "posts": posts_json,
                "last_id": posts[-1].id if posts else None
            })

        finally:
            session.close()

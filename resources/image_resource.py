from flask_restful import Resource, abort
from flask import Response

from data.db_session import create_session
from data.__all_models import Image


class ImageResource(Resource):
    def get(self, post_id):
        session = create_session()
        image = session.query(Image).filter_by(post_id=post_id).first()
        if image:
            return Response(image.content, mimetype=image.mime)
        return abort(404, message='Not found')

import sqlalchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    contents = sqlalchemy.Column(sqlalchemy.String)
    topic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    creation_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

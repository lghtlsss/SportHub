from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Comments'
    id = Column(Integer, autoincrement=True, primary_key=True)
    post_id = Column(Integer, ForeignKey("Posts.id"))
    author_id = Column(Integer)
    content = Column(String)
    creation_time = Column(DateTime, default=datetime.now)
    post = relationship('Post', back_populates='comments')

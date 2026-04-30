from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Likes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    post_id = Column(Integer, ForeignKey('Posts.id'))
    user = relationship('User', uselist=False, back_populates='likes')
    post = relationship('Post', back_populates='likes')
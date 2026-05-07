from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, String, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('Posts.id'))
    content = Column(LargeBinary)
    post = relationship('Post', back_populates='image')

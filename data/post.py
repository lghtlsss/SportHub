from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    author_id = Column(Integer)
    title = Column(String)
    text = Column(String)
    topic = Column(String, nullable=True)
    creation_time = Column(DateTime, default=datetime.now)
    comments = relationship('Comment', cascade='all, delete-orphan', lazy='selectin', back_populates='post')
    likes = relationship('Like', cascade='all, delete-orphan', lazy='selectin', back_populates='post')
    image = relationship('Image', back_populates='post', cascade='all, delete-orphan',uselist=False)

    def __repr__(self):
        return f'{self.id};{self.author};{self.title};{self.text};{self.image.id}'

from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Avatar(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Avatars'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(LargeBinary)
    mime = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))

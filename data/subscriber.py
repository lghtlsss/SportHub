from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Subscriber(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Subscribers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    subscriber_user_id = Column(Integer)
    user = relationship('User', back_populates='subscribers')

    def __repr__(self):
        return f'{self.user.name} {self.user.surname}'

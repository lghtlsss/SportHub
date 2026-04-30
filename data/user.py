import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pref_sport = sqlalchemy.Column(sqlalchemy.String)
    user = relationship('Like', back_populates='users')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

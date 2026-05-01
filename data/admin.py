import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Admins'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    rights_class = sqlalchemy.Column(sqlalchemy.Integer, default=2)  # 1 > 2

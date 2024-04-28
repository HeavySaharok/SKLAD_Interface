import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class InvModel(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'WARE_C'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, unique=True, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f'<Item> {self.id}'

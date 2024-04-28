import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class WareModel(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'warehouses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    coords = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fullness = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<Item> {self.id}'

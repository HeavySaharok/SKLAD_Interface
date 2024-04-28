import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class ItemModel(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'warehouses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    coords = sqlalchemy.Column()

    def __repr__(self):
        return f'<Item> {self.id}'

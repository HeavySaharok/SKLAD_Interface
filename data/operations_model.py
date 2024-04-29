import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class OperationModel(SqlAlchemyBase, UserMixin, SerializerMixin):
    """
    Модель cклада
    """
    __tablename__ = 'operations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    prod_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    res_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    send = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    receive = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Item> {self.id}'

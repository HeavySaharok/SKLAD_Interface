import sqlalchemy
from data.db_session import SqlAlchemyBase


class Ware(SqlAlchemyBase):
    __tablename__ = 'Ware'

    id = sqlalchemy.Column(sqlalchemy.Text, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    ware_id = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CarAd(Base):
    __tablename__ = 'car_ad'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=False)
    url = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

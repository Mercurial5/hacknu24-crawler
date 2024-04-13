from sqlalchemy import BigInteger, Column, String

from db.models.base import Base


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)

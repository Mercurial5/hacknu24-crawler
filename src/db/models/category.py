from sqlalchemy import Column, BigInteger, String

from db.models.base import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)

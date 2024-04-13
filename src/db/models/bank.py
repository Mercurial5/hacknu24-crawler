from sqlalchemy import BigInteger, Column, String

from db.models.base import Base


class Bank(Base):
    __tablename__ = 'bank'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)

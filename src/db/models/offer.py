from sqlalchemy import Column, BigInteger, ForeignKey, SmallInteger, DATETIME, String

from db.models.base import Base


class Offer(Base):
    __tablename__ = 'offer'

    id = Column(BigInteger, primary_key=True)
    category_id = Column(ForeignKey('category.id'), nullable=False)
    shop_id = Column(ForeignKey('shop.id'), nullable=False)
    bank_id = Column(ForeignKey('bank.id'), nullable=False)
    bonus = Column(SmallInteger, nullable=False)
    period = Column(String(255), nullable=True)
    updated_at = Column(DATETIME)

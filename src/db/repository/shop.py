from db import PostgresDB
from db.models import Shop


class ShopRepository:

    def __init__(self, db: PostgresDB):
        self._db = db

    def get_or_create(self, name: str) -> Shop:
        with self._db.session_scope() as session:
            if shop := session.query(Shop).filter_by(name=name).first():
                return shop

            shop = Shop(name=name)
            session.add(shop)

        return shop

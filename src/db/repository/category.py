from db import PostgresDB
from db.models import Category


class CategoryRepository:

    def __init__(self, db: PostgresDB):
        self._db = db

    def get_or_create(self, name: str) -> Category:
        with self._db.session_scope() as session:
            if category := session.query(Category).filter_by(name=name).first():
                return category

            category = Category(name=name)
            session.add(category)

        return category


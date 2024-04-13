from db import PostgresDB
from db.models import Bank


class BankRepository:
    def __init__(self, db: PostgresDB):
        self._db = db

    def get_or_create(self, name: str) -> Bank:
        with self._db.session_scope() as session:
            if bank := session.query(Bank).filter_by(name=name).first():
                return bank

            bank = Bank(name=name)
            session.add(bank)

        return bank

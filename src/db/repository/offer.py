from datetime import datetime

from db import PostgresDB
from db.models import Offer
from db.repository import CategoryRepository, ShopRepository, BankRepository
from dto import OfferDTO


class OfferRepository:
    def __init__(self,
                 db: PostgresDB,
                 category_repository: CategoryRepository,
                 shop_repository: ShopRepository,
                 bank_repository: BankRepository
                 ):
        self._db = db
        self._category_repository = category_repository
        self._shop_repository = shop_repository
        self._bank_repository = bank_repository

    def create_or_update_offer(self, offer_dto: OfferDTO) -> Offer:
        category = self._category_repository.get_or_create(offer_dto.category)
        shop = self._shop_repository.get_or_create(offer_dto.shop)
        bank = self._bank_repository.get_or_create(offer_dto.bank)

        with self._db.session_scope() as session:
            query = session.query(Offer).filter_by(category_id=category.id, shop_id=shop.id, bank_id=bank.id)

            existing_offer: Offer = query.first()
            if not existing_offer:
                offer = Offer(category_id=category.id, shop_id=shop.id, bank_id=bank.id, bonus=offer_dto.bonus)
            else:
                existing_offer.bonus = offer_dto.bonus
                offer = existing_offer

            offer.updated_at = datetime.now()

            session.add(offer)

        return offer

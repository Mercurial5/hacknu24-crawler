import json

from crawler import KaspiAICrawler, KaspiCrawler, HalykCrawler, JusanCrawler
from db import PostgresDB, PostgresConfigs
from db.repository import OfferRepository, CategoryRepository, ShopRepository, BankRepository


def main():
    postgres_configs = PostgresConfigs.from_environ()
    db = PostgresDB(postgres_configs)

    category_repository = CategoryRepository(db)
    shop_repository = ShopRepository(db)
    bank_repository = BankRepository(db)

    offer_repository = OfferRepository(db, category_repository, shop_repository, bank_repository)

    with open('rules/kaspi.json') as file:
        kaspi_rules = json.load(file)

    with open('rules/halyk.json') as file:
        halyk_rules = json.load(file)

    with open('rules/jusan.json') as file:
        jusan_rules = json.load(file)

    kaspi_crawler = KaspiCrawler()
    for offer in kaspi_crawler.get_offers(kaspi_rules):
        offer_repository.create_or_update_offer(offer)

    halyk_crawler = HalykCrawler()
    for offer in halyk_crawler.get_offers(halyk_rules):
        offer_repository.create_or_update_offer(offer)

    jusan_crawler = JusanCrawler()
    for offer in jusan_crawler.get_offers(jusan_rules):
        offer_repository.create_or_update_offer(offer)

    kaspiai_crawler = KaspiAICrawler()
    for offer in kaspiai_crawler.get_offers():
        print(offer)
        offer_repository.create_or_update_offer(offer)


if __name__ == '__main__':
    main()

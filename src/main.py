import json

from crawler import KaspiCrawler, HalykCrawler
from db import PostgresDB, PostgresConfigs
from db.repository import OfferRepository


def main():
    with open('rules/kaspi.json') as file:
        kaspi_rules = json.load(file)

    with open('rules/halyk.json') as file:
        halyk_rules = json.load(file)

    kaspi_crawler = KaspiCrawler()
    offers = list(kaspi_crawler.get_offers(kaspi_rules))

    halyk_crawler = HalykCrawler()
    offers.extend(halyk_crawler.get_offers(halyk_rules))

    print(offers)

    postgres_configs = PostgresConfigs.from_environ()
    db = PostgresDB(postgres_configs)
    offer_repository = OfferRepository(db)
    for offer in offers:
        offer_repository.create_or_update_offer(offer)


if __name__ == '__main__':
    main()
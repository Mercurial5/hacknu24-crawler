import re
from typing import Iterator

from crawler.crawler import Crawler
from dto import OfferDTO


class HalykCrawler(Crawler):
    def _get_discount(self, category: str, *args) -> int | None:
        pass

    def _create_offer(self, category: str, merchant: str, discount: int) -> OfferDTO:
        pass

    HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru',
        'authorization': 'Bearer XJSOCV68PKMCQQXIOYIFJW',
        'city_id': '1501',
        'dnt': '1',
        'origin': 'https://halykbank.kz',
        'referer': 'https://halykbank.kz/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    LINK = 'https://pelican-api.homebank.kz/halykclub-api/v1/terminal/merchants'
    BANK_NAME = 'Халык'

    def get_offers(self, rules: list[dict]) -> Iterator[OfferDTO]:
        for rule in rules:
            for merchant in self.__get_merchants(rule['categoryId']):
                target = None
                for tag in merchant['tags']:
                    if tag['code'] == 'bonus':
                        target = tag
                        break

                if target is None:
                    continue

                bonus = int(re.search(r'\d*', target['text']).group())
                yield OfferDTO(category=rule['categoryName'], shop=merchant['name'], bank=self.BANK_NAME, bonus=bonus)

    def __get_merchants(self, category: str) -> Iterator[dict]:
        params = dict(category_code=category)
        for page in range(1, 4):
            response = self._send_request('GET', self.LINK, params=params, headers=self.HEADERS)
            yield from response.json()['data']

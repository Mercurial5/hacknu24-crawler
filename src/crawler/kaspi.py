import re
from typing import Iterator

from crawler.crawler import Crawler
from dto import OfferDTO


class KaspiCrawler(Crawler):
    HEADERS = {
        'Accept': 'application/json, text/*',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Referer': 'https://kaspi.kz/shop/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    PARAMS = {
        'text': '',
        'sort': 'relevance',
        'qs': '',
        'ui': 'd',
        'i': '-1',
    }
    LINK = 'https://kaspi.kz/yml/product-view/pl/results'
    BANK_NAME = 'Каспи'

    def _get_discount(self, category: str, merchant: str) -> int | None:
        for product in self.__get_products(category, merchant):
            if discount := self._fetch_discount(product):
                return discount

    def _create_offer(self, category: str, merchant: str, discount: int) -> OfferDTO:
        return OfferDTO(category=category, shop=merchant, bank=self.BANK_NAME, bonus=discount)

    def __get_products(self, category: str, merchant: str) -> Iterator[dict]:
        params = self.PARAMS.copy()
        params['q'] = f':category:{category}:allMerchants:{merchant}'

        for page in range(1, 4):
            params['page'] = str(page)
            response = self._send_request('GET', self.LINK, headers=self.HEADERS, params=params)
            if not response:
                continue

            yield from response.json()['data']

    @staticmethod
    def _fetch_discount(product: dict) -> int | None:
        if 'promo' not in product:
            return None

        for promo in product['promo']:
            if '%' in promo['code']:
                percent = re.search(r'\d*', promo['code'])
                if percent:
                    return int(percent.group())

        return None

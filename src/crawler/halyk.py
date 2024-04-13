import re
from typing import Iterator

from crawler.crawler import Crawler
from dto import OfferDTO


class HalykCrawler(Crawler):
    HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://halykmarket.kz',
        'Referer': 'https://halykmarket.kz/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    PARAMS = {
        'page': '1',
        'sort_by': 'relevance',
        'order': 'asc',
        'extended': 'true',
    }
    LINK = 'https://api-r46.halykmarket.kz/products'
    BANK_NAME = 'Халык'

    def __init__(self):
        super().__init__()
        self._shop_id = self.__get_shop_id()
        self.PARAMS['shop_id'] = self._shop_id

    def _get_discount(self, category: str, merchant: str) -> int | None:
        for product in self.__get_products(category, merchant):
            if 'discount' in product:
                return int(product['discount'])

    def _create_offer(self, category: str, merchant: str, discount: int) -> OfferDTO:
        return OfferDTO(category=category, shop=merchant, bank=self.BANK_NAME, bonus=discount)

    def __get_products(self, category: str, merchant: str) -> Iterator[dict]:
        params = self.PARAMS.copy()
        params['categories'] = category
        params['filters'] = f'{{"merchantName":["{merchant}"]}}'

        for page in range(1, 4):
            params['page'] = str(page)
            response = self._send_request('GET', self.LINK, params=params, headers=self.HEADERS)
            yield from response.json()['products']

    def __get_shop_id(self) -> str:
        response = self._send_request('GET', 'https://halykmarket.kz/category/telefoni-i-gadzheti')
        if not response:
            return '693ff081028570920fd8a6b971eb5e'

        shop_id = re.search(r'(?<=SHOP_ID:").*?(?=")', response.text)
        if not shop_id:
            return '693ff081028570920fd8a6b971eb5e'

        return shop_id.group()

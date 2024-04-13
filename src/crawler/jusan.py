import re
from typing import Iterator

from crawler.crawler import Crawler
from dto import OfferDTO


class JusanCrawler(Crawler):
    COOKIES = {
        'PROD-fingerprint': '%228a86f44e3b233f93bb3f1a2415e5f3e5%22',
        'yohe_uid': '33ac3d00-f980-11ee-9d8e-117fa3f10a9b',
        'yohe_uid': '33ac3d00-f980-11ee-9d8e-117fa3f10a9b',
        'AMP_MKTG_97c0cadc7f': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmp1c2FuLmt6JTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMmp1c2FuLmt6JTIyJTdE',
        'AMP_MKTG_97c0cadc7f': 'JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmp1c2FuLmt6JTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMmp1c2FuLmt6JTIyJTdE',
        '_gcl_au': '1.1.1191966828.1713003955',
        '_gcl_au': '1.1.1191966828.1713003955',
        '_ga': 'GA1.1.609010143.1712998052',
        '_ga': 'GA1.1.609010143.1712998052',
        '_fbp': 'fb.1.1713003955345.21373709',
        '_ym_uid': '1713003955864720797',
        '_ym_d': '1713003955',
        '_fbp': 'fb.1.1713003955345.21373709',
        '_ym_uid': '1713003955864720797',
        '_ym_d': '1713003955',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        '_ym_isad': '2',
        'PROD-APP-SELECTED-CITY-V3': '{%22id%22:%2213698%22%2C%22name%22:%22%D0%90%D1%81%D1%82%D0%B0%D0%BD%D0%B0%22}',
        '_ym_visorc': 'w',
        'review_service_session': 'aF78MFSKQaCAAZtToCHnBvr21GDl1qeHT9heWkT5',
        'BNES_review_service_session': 'mEbJxte0vuE0jpkTbjrN4+R+EnbzeppHhwfag4/vaIGFV0Zr3m/XiVvMnCTPOpwggPAiTmtGs+mKSn5gdp9AIQWAOSUhP9Xw5QN18OtsCNpo1pTjrK6Ebmx1BrqLUz8RH3/LrHqP8uPsxm6ukCBJzQ==',
        'cart_service_session': 'gYTo0TkDP0vUIpOxddXwtnSsIbY6EAoXGX17Fk6z',
        'BNES_cart_service_session': 'YVwUZioxm8p8GQl2kcvqu5b6N0hC5NkB2zvRJcVL4yCu/R5w3BVJX8kuXk2ZjKVOEWmg5e6g+y3D5accZdYIoKzA1xlmSCBodcKNwZSZP3DJmCH4f53vIej2YB9+GcogXiay1RtNmYs=',
        '_ga_BC841VM9TH': 'GS1.1.1713014907.2.1.1713019076.43.0.2125906888',
        'AMP_97c0cadc7f': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0ODAwZDVhOC0wZDg5LTRkMTgtYTBiZS0yM2NiNWRiMDUwOGUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzEzMDE0OTEzMDc4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxMzAxOTA3ODQyMiUyQyUyMmxhc3RFdmVudElkJTIyJTNBNTElN0Q=',
        'BNES_yohe_uid': 'ohVfWiNPpQ7ZtEsCqyKQun1k2q9fyrRdIwUSKKhXr7fo1t2MaDfRTLVklikwtkdMcspDWn1dqFz/qTib7szYDie+1quE09hVEsMfUVu1dxPwRD4LDmU9fQ==',
        'BNES_AMP_MKTG_97c0cadc7f': 'dRCygSnZZP7pzp0Iewn4hin0tDAlDwgd1eD4FU4sXTtj8lCM51IcLQBUbwtDHXVTj7BeI7O5rt7mZb9Vs7dlNxlgSmDPZ0URLpp/oG/r3/PXNlPdne4FHHjNWN40nZuw7kQaHHEwuR0nAYVFNL9WDg02JwoIj1Me2MduQ27UDPdfp/ilH8plTqgN9zelbUwaVlPEhVlVn56dCBFeWB9W3pW9DSpXzQQrXPJBw+BZQC0opXKdn9jwaKiEXAAoIZk7',
        'BNES__gcl_au': '1DdO/Kk4+dE+o4yOdsQbus/GWN9OVJzevhSCcm9W6mLygm5AgBKomFNtt5csl9U1zHMfaEqbHTH8/hetahAy9OGRBg02EGdd7tDV+QczzHU=',
        'BNES__ga': 'yx4mBU7lSJ42kP448pOWxHDw8tKWNGpsEHfmm56hray/AceEZjhEk4pz8NBtEuDkN5y+QUC6OlPgHWMAR0wfM1ISeakUEaAuK9c1sYlQ8jQ=',
        'BNES__fbp': 'GXdER78k+GP7pdCx9eSqW7tOITUZxy/mfrAGYJmbtjuvHLPiTLpHdEQvomixAUWDwRns8zrRHVUcYMoWtvdOLi9+ueZlcqphJDS8CgHRf5M=',
        'BNES__ym_uid': 'Lm9oX8rpN2ze0VC1FiDM90O5lBhGP+36eqBRzy/SZF+2NL640JLrMfhFe++XCJ4zRpV4QJNVNSdGTAsFJCo2gLSgyOPxcjP+',
        'BNES__ym_d': 'wTXIlvYb3ZQivbfyOIYeWXG/gN/bGbC1HL9bLrvVMVpo69aKC4ut5WS7k/QHavSttLjsOYYKtSXar9mN2JD2lA==',
        'BNES__ym_isad': 'VVTIIBzNfLNoX56PlQbAYaK0Fzuj0iGmNd8SQlu4nDYlqXkyezmCrMYU1MYExsi6dWVUa+85+aQ=',
        'BNES__ym_visorc': 'rYqKA7HuBm4L5FeRx0PyRKq3iCihs8NU2dg1/fV4EBbEQox3laZ/xQPUa1xK+KWjrQEW9oimYCQ=',
        'BNES__ga_BC841VM9TH': 'EaEDfI5g8MzzDQyMAAxzuilgRsDVD4emfrOoGZ+ABFQie9uGLm4ORiBnSwkmxLIny7lQphhscPhDirtuJRgZ/PYs8DNOnrkkU3rQkWcn+PfUikIWc4fFujCI9ZuzCv8iSiYA9w9G9GAmAU16SV2bHQ==',
        'BNES_AMP_97c0cadc7f': 'm2BEir9fzv6uYsLkHiC64cPs7Z+g1vaE8LYdcZHKBl2JUULAXwilH6nANeaVRr50bHuNgjODwgHgEpK3ahpXx9AxQNxM6Ng/eXBzlfXgf6OHp+5Mwu/eXZJ+7se+uRTeAGQol0dfm5QjxXWDUYo7NUN7CH5CCvGcB+zI+HMT6bw/rO7ua4gO/+iQkyaqrWJQXv/i84M9WbtQphbgdHkWEu5I2592vM1weqVBeE65pSCSjS1pB/SyNKH1xSevCbxnxiMGeaTO1dcT/SaoRUaE7lENAsYjwCkBM6iE3nofQCj4aj4u63usMkBRL37dgr/xlttHirt2Ty5BXdpT3kOJgXvB3J3jby2VQPI0r++BVq0hl0834EaHJU6kVCty1Gex/L7wYUWXgBadIiBLbkfGh87kYvf2hcA9',
        'AMP_97c0cadc7f': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0ODAwZDVhOC0wZDg5LTRkMTgtYTBiZS0yM2NiNWRiMDUwOGUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzEzMDE0OTEzMDc4JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxMzAxOTExODQ0OCUyQyUyMmxhc3RFdmVudElkJTIyJTNBNTIlN0Q=',
        '_ga_BC841VM9TH': 'GS1.1.1713014907.2.1.1713019118.1.0.2125906888',
    }
    HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-language': 'ru',
        'Appsflyer-segment': 'A',
        'City-Id': '13698',
        'Connection': 'keep-alive',
        'Fingerprint-Id': '8a86f44e3b233f93bb3f1a2415e5f3e5',
        'Platform': 'DESKTOP',
        'Referer': 'https://jmart.kz/products?category_id=1391',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Storefront-Api-Access-Key': '91356a96edd62b929a9e5573d6585261',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    PARAMS = {
        'category_id': '1391',
        'show_totals': 'true',
    }
    LINK = 'https://jmart.kz/gw/listing/v1/products'
    BANK_NAME = 'Жусан'

    def _get_discount(self, category: str, merchant: str) -> int | None:
        for product in self.__get_products(category, merchant):
            if discount := self._fetch_discount(product):
                return discount

    def _create_offer(self, category: str, merchant: str, discount: int) -> OfferDTO:
        return OfferDTO(category=category, shop=merchant, bank=self.BANK_NAME, bonus=discount)

    def __get_products(self, category: str, merchant: str) -> list[dict]:
        params = self.PARAMS.copy()
        params['q'] = f':category:{category}:allMerchants:{merchant}'
        result = []
        for page in range(1, 4):
            params['page'] = str(page)
            response = self._send_request('GET', self.LINK, headers=self.HEADERS, params=params)

            if not response.ok:
                continue
            result.append(response.json()['data'])
        return result

    @staticmethod
    def _fetch_discount(product: dict) -> int | None:
        if not product.get('products'):
            return None
        for product in product['products']:
            for label in product['labels']:
                if '%' in label['label_name']:
                    percent = re.search(r'\d*', label['label_name'])
                    if percent:
                        return int(percent.group())

        return None


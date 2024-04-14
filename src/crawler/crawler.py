from abc import ABC, abstractmethod
from typing import Iterator

import requests
from requests import Response, Session, RequestException

from dto import OfferDTO


class Crawler(ABC):

    def __init__(self, session: Session | None = None):
        self.__session = session if session else requests

    def get_offers(self, rules: list[dict]) -> Iterator[OfferDTO]:
        for rule in rules:
            for merchant in rule['merchants']:
                if discount := self._get_discount(rule['categoryId'], merchant['id']):
                    yield self._create_offer(rule['categoryName'], merchant['name'], discount)

    @abstractmethod
    def _get_discount(self, category: str, *args) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def _create_offer(self, category: str, merchant: str, discount: int) -> OfferDTO:
        raise NotImplementedError

    def _send_request(self, method: str, link: str, **kwargs) -> Response | None:
        for _ in range(3):
            try:
                return self.__session.request(method, link, **kwargs)
            except RequestException:
                continue

        return None

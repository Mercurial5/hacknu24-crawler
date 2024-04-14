import io
import json
from os import environ
from typing import Iterator

import PIL
import google.generativeai as genai
import requests

from dto import OfferDTO

GOOGLE_API_KEY = environ['GOOGLE_API_KEY']


class KaspiAICrawler:
    categories = """
    Телефоны и гаджеты
    Бытовая техника
    ТВ, Аудио, Видео
    Компьютеры
    Мебель
    Красота, здоровье
    Детские товары
    Аптека
    Строительство, ремонт
    Спорт, туризм
    Досуг, книги
    Автотовары
    Украшения
    Аксессуары
    Одежда
    Обувь
    Товары для дома и дачи
    Товары для животных
    Подарки, товары для праздников
    Канцелярские товары
"""

    def __init__(self):
        self.api_key = GOOGLE_API_KEY

    def get_data(self):
        headers = {
            'Host': 'pcm.kaspi.kz',
            'X-Locale': 'ru-RU',
            'X-Call': '-1|audioMode=0',
            'X-Install-Id': 'e7cf6b8b-2e64-461e-9f09-0e4feb296e11',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'okhttp/4.12.0',
            'Connection': 'close',
        }

        response = requests.get(
            'https://pcm.kaspi.kz/mpcm/api/v1.0/pcm/getCampaigns?Time=1970-01-01T00:00:00',
            headers=headers
        )
        if not response.ok:
            raise Exception('Failed to get data from Kaspi')

        return response.json()

    def get_offers(self) -> Iterator[OfferDTO]:
        result = self.get_data()

        if not result.get('data'):
            raise Exception('No data in response')

        campaigns = result['data']['campaigns']

        if campaigns:
            counter = 0
            for campaign in campaigns:
                if not campaign.get('data'):
                    continue
                data = campaign['data']
                if not data.get('imageUrl'):
                    continue
                counter += 1
                model = genai.GenerativeModel('gemini-pro-vision')
                response = requests.get(data['imageUrl'])
                if "s.kaspi.kz/api/resources/6" in data['imageUrl']:
                    continue
                img = PIL.Image.open(io.BytesIO(response.content))
                a = """
                   Телефоны и гаджеты
                   Бытовая техника
                   ТВ, Аудио, Видео
                   Компьютеры
                   Мебель
                   Красота, здоровье
                   Детские товары
                   Аптека
                   Строительство, ремонт
                   Спорт, туризм
                   Досуг, книги
                   Автотовары
                   Украшения
                   Аксессуары
                   Одежда
                   Обувь
                   Товары для дома и дачи
                   Товары для животных
                   Подарки, товары для праздников
                   Канцелярские товары"""
                response = model.generate_content([
                    f"Если на фото будут цифры 0.0.12 то это значит что это рассрочка а не бонусы ! Если на фото будут % и потом цифра то значит там есть бонус. Подгони категории из фото в один из этих вариантов {a}. И после этого сформируй для меня json по этой модели category:str bonus:int \n\n",
                    img], stream=True)
                response.resolve()
                # print(response)
                print(response)
                result = json.loads(response.text.replace('```', '').replace('json', ''))
                if result['bonus'] == 0:
                    continue
                # need promt ISSUE BROOOO
                offer = OfferDTO(category=result['category'], shop='На все магазины', bank='Kaspi', bonus=result['bonus'], period=data['desc'])
                yield offer

            # offer = OfferDTO(
            #     category=self.categories,
            #     shop="179",
            #     bank='На все магазины',
            #     bonus=0,
            #     conditions=[],
            # )


if __name__ == '__main__':
    crawler = KaspiAICrawler()
    crawler.parse_data()

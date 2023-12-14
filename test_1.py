import pytest
import json

from classes_first_hometask_1 import Advert

def test_1():
    json_ad = {
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }
    advert = Advert(json_ad)
    assert advert.location.address == 'город Самара, улица Мориса Тореза, 50' and advert.price == 100

def test_2():
    json_ad = {
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }
    advert = Advert(json_ad)
    assert advert.location.address == 'сельское поселение Ельдигинское, поселок санатория Тишково, 25' and advert.price == 1000

def test_3():
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    assert lesson_ad.price == 0


def test_exp():
    with pytest.raises(ValueError):
        json_ad = {
            "title": "Вельш-корги",
            "price": -1,
            "class": "dogs",
            "location": {
                "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
            }
        }
        advert = Advert(json_ad)

def test_exp_2():
    with pytest.raises(ValueError):
        json_ad = {
            "title": "Вельш-корги",
            "price": 1000,
            "class": "dogs",
            "location": {
                "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
            }
        }
        advert = Advert(json_ad)
        advert.price = -3

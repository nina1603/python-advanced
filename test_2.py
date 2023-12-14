from classes_first_hometask_2 import Advert_2 as Advert

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
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
        }
    }
    advert = Advert(json_ad)
    assert advert.title == 'iPhone X' and advert.repr_color_code == 33

def test_3():
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
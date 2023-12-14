from classes_first_hometask_2 import Advert_2 as Advert

if __name__ == '__main__':
    ad = {
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs",
        "location": {
            "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
        }
    }

advert = Advert(ad)
print(advert)
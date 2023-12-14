from classes.classes_first_hometask_1 import Advert


class ColorizeMixin:
    repr_color_code = 33  # yellow

    def __repr__(self):
        color_option = f'\033[{self.repr_color_code}m{self.title} | {self.price} ₽'
        return color_option

class Advert_2(ColorizeMixin, Advert):
    """
    new class similar to Advert but printing coloured line with ad name and price
    """

    def __init__(self, json_obj):
        super().__init__(json_obj)

    def rename_attr(self, key):
        return super().rename_attr(key)
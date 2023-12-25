import keyword
from abc import ABC


class DictToObj(ABC):
    def __init__(self, json_obj):
        for key, val in json_obj.items():
            if not isinstance(val, (tuple, list)):
                setattr(
                    self,
                    self.rename_attr(key),
                    DictToObj(val) if isinstance(val, dict) else val)
            else:
                setattr(
                    self,
                    self.rename_attr(key),
                    [DictToObj(it) if isinstance(it, dict) else it for it in val])

    @staticmethod
    def rename_attr(key):
        """
        if is keyword add _ to the name
        """
        if keyword.iskeyword(key):
            return f'_{key}'
        return key


class Advert(DictToObj):
    """
    Creates attributes dynamically from json object
    Has additional price property for checking value and secure printing
    """
    def __init__(self, json_obj):
        super().__init__(json_obj)
        if not hasattr(self, 'title'):
            raise ValueError('No attribute `title` is found!')
        if hasattr(self, '_price') and self._price < 0:
            raise ValueError('Invalid value for `price`! Should be not less than zero.')
        if not hasattr(self, '_price'):
            self._price = 0

    def rename_attr(self, key):
        """
        in addition to the superior method changes attribute to secured one
        """
        key_renamed = super().rename_attr(key)
        if key_renamed == 'price':
            return f'_{key_renamed}'
        return key_renamed

    @property
    def price(self):
        """
        secured call for `price` attribute value
        """
        return self._price

    @price.setter
    def price(self, price):
        """
        secure `price` update
        """
        if price < 0:
            raise ValueError('Invalid value for `price`! Should be not less than zero.')
        self._price = price

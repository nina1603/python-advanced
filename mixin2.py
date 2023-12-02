from abc import ABC, abstractproperty, abstractstaticmethod, abstractmethod


class PokemonTrainInterface(ABC):
    @abstractmethod
    def increase_experience(self, value):
        pass

    @property
    @abstractmethod
    def experience(self):
        pass


class Pokemon(PokemonTrainInterface):
    def __init__(self, name: str, poketype: str):
        self.name = name
        self.poketype = poketype
        self._experience = 100

    def __str__(self):
        return f'{self.name}/{self.poketype}'

    def increase_experience(self, value: int):
        self.experience = self.experience + value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    bulbasaur.increase_experience(100)
    assert bulbasaur.experience == 200, 'Try harder, Neeman'
    print(bulbasaur)

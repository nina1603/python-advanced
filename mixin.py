class EmojiMixin():
    def __repr__(self):
        emoj = {
            'grass': '🌿',
            'fire': '🔥',
            'water': '🌊',
            'electric': '⚡️',
        }
        return f'{self.name} + {emoj[self.poketype]}'


class BasePokemon():
    def __init__(self, name: str, poketype: str):
        self.name = name
        self.poketype = poketype

    def __repr__(self):
        return f'{self.name}/{self.emoj[self.poketype]}'


class Pokemon(EmojiMixin, BasePokemon):
    pass


if __name__ == '__main__':
    bulbasaur = Pokemon(name='Bulbasaur', poketype='grass')
    print(bulbasaur)

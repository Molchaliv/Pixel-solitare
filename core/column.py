from pygame import rect

from .cards import Card_GameObject


class Column_GameObject(object):
    """ Class for managing columns. """

    def __init__(self, x: int, y: int, cards: list = []) -> None:
        """ Initialization function. """

        self._cards = cards

        self._rect = rect.Rect(x, y, 100, 2660)

    @property
    def rect(self) -> rect.Rect:
        return self._rect

    @property
    def cards(self) -> list[Card_GameObject]:
        return self._cards

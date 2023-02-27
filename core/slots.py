from pygame import rect, surface

from .cards import Card_GameObject


class Slot_GameObject(object):
    """ Class for creating side cells with cards. """

    def __init__(self, x: int, y: int) -> None:
        """ Initialization function. """

        self._cards = []
        self._remove_last = False

        self._rect = rect.Rect(x, y, 100, 140)

        self._x = x
        self._y = y

    @property
    def cards(self) -> list[Card_GameObject]:
        return self._cards

    @property
    def rect(self) -> rect.Rect:
        return self._rect

    def superimposed_card(self, cards: list[Card_GameObject]) -> bool:
        """ Returns a boolean value of whether a card can be placed in a cell. """

        if len(cards) != 1:
            return False

        card = cards[0]
        if card.value == "a":
            return True

        if self._cards:
            if card.index - 1 == self._cards[-1].index and card.suit == self._cards[-1].suit:
                return True

        return False

    def get_card(self, start_move: bool = True) -> Card_GameObject:
        """ Returns the last card in the list. """

        if start_move:
            self.start_move()

        return self._cards[-1]

    def add_card(self, card: Card_GameObject, system: bool = False) -> None:
        """ Adds a new card to the list. """

        if self.superimposed_card([card]) or system:
            self._cards.append(card)

    def remove_card(self, stop_move: bool = True) -> None:
        """ Removes the last card from the list. """

        if stop_move:
            self.stop_move()

        if self._cards:
            del self._cards[-1]

    def start_move(self) -> None:
        """ Starts the movement of the last card """

        self._remove_last = True

    def stop_move(self) -> None:
        """ Stops the movement of the last card. """

        self._remove_last = False

    def clear(self) -> None:
        """ Clears the entire list. """

        self._cards.clear()

        self.stop_move()

    def render(self, screen: surface.Surface) -> None:
        """ Renders in-class objects. """

        if self._remove_last:
            for card in self._cards[:-1]:
                card.move(self._x, self._y, True)
                card.render(screen)
        else:
            for card in self._cards:
                card.move(self._x, self._y, True)
                card.render(screen)

import random

from pygame import mouse, rect, surface, mixer

from .cards import Card_GameObject
from .column import Column_GameObject
from .slots import Slot_GameObject
from .statistic import Statistic_Game_Object


def superimposed(cards: list[Card_GameObject], column: Column_GameObject) -> bool:
    """ Returns a boolean value of whether a card can be placed in a column. """

    if not cards or not column.rect.collidepoint(*mouse.get_pos()):
        return False

    if not column.cards and cards[0].value == "k":
        return True

    if column.cards:
        if cards[0].index == column.cards[-1].index - 1 and cards[0].color != column.cards[-1].color:
            return True

    return False


class Field_GameObject(object):
    """ The main class responsible for the entire gameplay. """

    def __init__(self, assets: str = ".\\assets") -> None:
        """ Initialization function. """

        self._cards = []
        for suit in ["hearts", "spades", "diamonds", "clubs"]:
            for value in ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "k", "q"]:
                self._cards.append(
                    Card_GameObject(f"{assets}\\{suit}\\{value}.png", f"{assets}\\back.png", value, suit)
                )

        self._statistic = Statistic_Game_Object(15, 525, assets=assets)

        self._shuffle = mixer.Sound(f"{assets}\\sounds\\shuffle.wav")
        self._flip = mixer.Sound(f"{assets}\\sounds\\flip.wav")

        self._field = []
        self._magazine = []
        self._slots = [
            Slot_GameObject(1165, 15),
            Slot_GameObject(1165, 170),
            Slot_GameObject(1165, 325),
            Slot_GameObject(1165, 480)
        ]

        self._magazine_rect = rect.Rect(15, 15, 100, 140)

        self._move_pos = (0, 0)
        self._cards_move = []

        self.shuffle_cards()

    @property
    def cards(self) -> list[Card_GameObject]:
        return self._cards

    @property
    def ended(self) -> bool:
        if not self._magazine:
            return False

        if not self._magazine[0] and not self._magazine[1] and all([card.front for card in self._cards]):
            return True

        return False

    def get_cards(self) -> list[Card_GameObject]:
        """ Returns cards to move around the playing field. """

        x, y = mouse.get_pos()

        for index_0, column in enumerate(self._field):
            for index_1, card in list(enumerate(column.cards))[::-1]:
                if card.front and card.rect.collidepoint(x, y):
                    self._move_pos = (index_0, index_1)

                    return column.cards[index_1:]

        for index_0, slot in enumerate(self._slots):
            if slot.cards and slot.rect.collidepoint(x, y):
                self._move_pos = (-(index_0 + 2), -(index_0 + 2))

                return [slot.get_card()]

        if self._magazine[1]:
            if self._magazine[1][-1].rect.collidepoint(x, y) and not self._magazine_rect.collidepoint(x, y):
                self._move_pos = (-1, -1)

                return [self._magazine[1][-1]]

        return []

    def start_cards_move(self) -> list[Card_GameObject]:
        """ Starts card movement. """

        self._cards_move = self.get_cards()
        for card in self._cards_move:
            card.set_movable(True)

        return self._cards_move

    def stop_cards_move(self) -> None:
        """ Completes the movement of cards and distributes them across the field. """

        x, y = mouse.get_pos()

        for slot in self._slots:
            slot.stop_move()

            if slot.rect.collidepoint(x, y) and slot.superimposed_card(self._cards_move):
                self.remove_duplicates()
                self.add_statistic()

                slot.add_card(self._cards_move[0])

        for index_0, column in enumerate(self._field):
            if superimposed(self._cards_move, column):
                self.remove_duplicates()
                self.add_statistic()

                self._field[index_0].cards.extend(self._cards_move)

        for column in self._field:
            if column.cards:
                column.cards[-1].set_front()

        for card in self._cards_move:
            card.set_movable(False)

        self._cards_move = []

    def remove_duplicates(self) -> None:
        """ Cleans up duplicate cards in lists. """

        if self._move_pos[0] == -1:
            del self._magazine[1][-1]
        elif self._move_pos[0] == -2:
            self._slots[0].remove_card()
        elif self._move_pos[0] == -3:
            self._slots[1].remove_card()
        elif self._move_pos[0] == -4:
            self._slots[2].remove_card()
        elif self._move_pos[0] == -5:
            self._slots[3].remove_card()
        else:
            if self._move_pos == 0:
                self._field[self._move_pos[0]].cards.clear()
            else:
                del self._field[self._move_pos[0]].cards[self._move_pos[1]:]

    def add_statistic(self) -> None:
        """ Updates statistics. """

        self._statistic.add_step()
        self._flip.play()

    def new_card(self, system: bool = False) -> None:
        """ Pulls out a new card from the store. """

        if self._magazine_rect.collidepoint(*mouse.get_pos()) or system:
            if not self._magazine[0]:
                self.add_statistic()

                self._magazine[0].extend(self._magazine[1])
                self._magazine[1].clear()

                for card in self._magazine[0]:
                    card.set_back()
            else:
                self.add_statistic()

                self._magazine[1].append(self._magazine[0][-1])
                self._magazine[1][-1].set_front()
                self._magazine[0].pop()

    def shuffle_cards(self) -> None:
        """ Shuffles cards and erases progress. """

        random.shuffle(self._cards)

        self._statistic.start_record(self.ended)
        self._shuffle.play()

        self._field.clear()
        self._magazine.clear()

        for slot in self._slots:
            slot.clear()

        for card in self._cards:
            card.set_back()

        self._field.append(Column_GameObject(185, 15, self._cards[:1]))
        self._field.append(Column_GameObject(320, 15, self._cards[1:3]))
        self._field.append(Column_GameObject(455, 15, self._cards[3:6]))
        self._field.append(Column_GameObject(590, 15, self._cards[6:10]))
        self._field.append(Column_GameObject(725, 15, self._cards[10:15]))
        self._field.append(Column_GameObject(860, 15, self._cards[15:21]))
        self._field.append(Column_GameObject(995, 15, self._cards[21:28]))

        self._field[0].cards[-1].set_front()
        self._field[1].cards[-1].set_front()
        self._field[2].cards[-1].set_front()
        self._field[3].cards[-1].set_front()
        self._field[4].cards[-1].set_front()
        self._field[5].cards[-1].set_front()
        self._field[6].cards[-1].set_front()

        self._magazine.append(self._cards[28:])
        self._magazine.append([])

    def place_cards(self):  # contains unused tools
        """ Places cards on the playing field. """

        for x, column in enumerate(self._field):
            for y, card in enumerate(column.cards):
                card.move((x * 135) + 185, (y * 35) + 15, True)

                # card.set_animation(
                #     point_path(card.rect.x, card.rect.y, (x * 135) + 185, (y * 35) + 15)
                # )

        for card in self._magazine[0]:
            card.move(15, 15, True)

        for y, card in enumerate(self._magazine[1][-3:]):
            card.move(15, 175 + (y * 35), True)

    def render(self, screen: surface.Surface, auto_place: bool = True) -> None:
        """ Renders in-class objects. """

        if auto_place and not self._cards_move:
            self.place_cards()

        self._statistic.render(screen)

        for column in self._field:
            for card in column.cards:
                if not card.movable:
                    card.render(screen)

        for card in self._magazine[0]:
            card.render(screen)

        for card in self._magazine[1][-3:]:
            card.render(screen)

        for slot in self._slots:
            slot.render(screen)

        for card in self._cards_move:
            card.render(screen)

from pygame import image, transform, rect, surface


_cards = ["a", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]  # all cards short name


class Card_GameObject(object):
    """ Class for managing and interacting with cards """

    def __init__(self, front: str, back: str, value: str = "a", suit: str = "hearts") -> None:
        """ Initialization function. """

        self._front = transform.scale(image.load(front), (100, 140))
        self._back = transform.scale(image.load(back), (100, 140))

        self._value = value
        self._suit = suit
        self._movable = False

        self._animation = []

        self._base_image = self._back
        self._base_rect = self._base_image.get_rect()

    @property
    def value(self) -> str:
        return self._value

    @property
    def index(self) -> int:
        return _cards.index(self._value)

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def movable(self) -> bool:
        return self._movable

    @property
    def rect(self) -> rect.Rect:
        return self._base_rect

    @property
    def front(self) -> bool:
        if self._base_image == self._front:
            return True
        return False

    @property
    def color(self) -> str:
        if self._suit in ["spades", "clubs"]:
            return "black"
        return "red"

    def set_front(self) -> None:
        """ Flips the card to face the camera. """

        self._base_image = self._front

    def set_back(self) -> None:
        """ Flips the card back to the camera """

        self._base_image = self._back

    def flip_card(self) -> None:
        """ Expands the card. """

        if self._base_image == self._front:
            self._base_image = self._back
        else:
            self._base_image = self._front

    def set_animation(self, animation: list[tuple[int, int]]) -> None:  # contains unused tools
        """ Creates an animation ( position is updated with each subsequent render ). """

        self._animation = animation

    def set_movable(self, state: bool) -> None:
        """ Toggles the value of the ability to move the map ( the value will be ignored on a system call ). """

        self._movable = state

    def move(self, x: int, y: int, system: bool = False) -> None:  # contains unused tools
        """ Moves the map to the specified position ( does not work when <movable is False> ). """

        if not system:
            self._animation = []

        if self._movable or system:
            self._base_rect = rect.Rect(x, y, self._base_rect.width, self._base_rect.height)

    def move_ip(self, x: int, y: int, system: bool = False) -> None:  # contains unused tools
        """ Moves the map to a given position relative to the cursor ( does not work when <movable is False> ). """

        if not system:
            self._animation = []

        if self._movable or system:
            self._base_rect.move_ip(x, y)

    def render(self, screen: surface.Surface) -> None:  # contains unused tools
        if self._animation:
            self.move(*self._animation[-1], system=True)

            del self._animation[-1]

        screen.blit(self._base_image, self._base_rect)

    def __str__(self) -> str:
        return f"Card_GameObject<value=\"{self._value}\", suit=\"{self._suit}\", front={self.front}>"

    def __repr__(self) -> str:
        return f"Card_GameObject<value=\"{self._value}\", suit=\"{self._suit}\", front={self.front}>"

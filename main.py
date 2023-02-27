import pygame
import sys

from core import Field_GameObject, Menu_GameObject


class Main(object):
    """ Class to initialize the main game. """

    def __init__(self, size: tuple[int, int]) -> None:
        """ Initialization function. """

        pygame.init()

        self._surface = pygame.display.set_mode(size)

        self._cards = Field_GameObject(".\\assets")
        self._menu = Menu_GameObject(0, 656, self._cards)
        self._moving = []

        pygame.display.set_caption("Solitaire")
        pygame.display.set_icon(pygame.image.load(".\\assets\\icon.png"))

    def exec(self):
        """ Renders in-game objects. """

        self._cards.render(self._surface)
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        sys.exit(pygame.quit())
                    case pygame.MOUSEBUTTONDOWN:
                        self._cards.new_card()
                        self._menu.check_buttons()

                        self._moving = self._cards.start_cards_move()
                    case pygame.MOUSEBUTTONUP:
                        self._moving = []
                        self._cards.stop_cards_move()
                    case pygame.MOUSEMOTION:
                        for card in self._moving:
                            card.move_ip(*event.rel)

            self._menu.render(self._surface)
            self._cards.render(self._surface)

            pygame.display.update()
            pygame.time.delay(5)


if __name__ == "__main__":
    main = Main((1280, 720))
    main.exec()

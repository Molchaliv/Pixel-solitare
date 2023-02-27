from pygame import surface, font


class Statistic_Game_Object(object):
    """ Class for managing game statistics. """

    def __init__(self, x: int, y: int, assets: str = ".\\assets") -> None:
        """ Initialization function. """

        self._font = font.Font(f"{assets}\\font.ttf", 20)

        self._rect = (x, y)

        self._x = x
        self._y = y

        self._best_score = 0
        self._score = 0

        with open("statistic.txt", mode="r", encoding="utf-8") as file:
            self._best_score = int(file.read().strip())

    def add_step(self) -> None:
        """ Adds 1 point to score. """

        self._score += 1

    def start_record(self, ended: bool = True) -> None:
        """ Erases the current score and updates the record if it has been broken. """

        if (self._score < self._best_score or self._best_score == 0) and ended:
            self._best_score = self._score
        self._score = 0

        with open("statistic.txt", mode="w", encoding="utf-8") as file:
            file.write(str(self._best_score))

    def render(self, screen: surface.Surface) -> None:
        """ Renders in-class objects. """

        screen.blit(self._font.render(f"Best: {self._best_score}", False, "white"), (self._x, self._y))
        screen.blit(self._font.render(f"Score: {self._score}", False, "white"), (self._x, self._y + 25))

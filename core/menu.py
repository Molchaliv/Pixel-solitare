from pygame import image, transform, rect, mixer, mouse, surface

from .field import Field_GameObject


class Menu_GameObject(object):
    """ Class to control some game settings. """

    def __init__(self, x: int, y: int, field: Field_GameObject, assets: str = ".\\assets") -> None:
        """ Initialization function. """

        self._field = field
        self._is_pause = False

        self._background = transform.scale(image.load(f"{assets}\\background.png"), (1280, 720))
        self._null = transform.scale(image.load(f"{assets}\\buttons\\null.png"), (64, 64))
        self._sound = transform.scale(image.load(f"{assets}\\buttons\\sound.png"), (64, 64))
        self._play = transform.scale(image.load(f"{assets}\\buttons\\play.png"), (64, 64))

        self._sound_rect = rect.Rect(x, y, 64, 64)
        self._play_rect = rect.Rect(x + 64, y, 64, 64)

        mixer.init()
        mixer.music.load(".\\assets\\sounds\\background-music.mp3")
        mixer.music.play(-1, 0.0)
        mixer.music.set_volume(0.5)

    def check_buttons(self) -> None:
        """ Checks for button presses. """

        if self._sound_rect.collidepoint(*mouse.get_pos()):
            self._is_pause = not self._is_pause
            if self._is_pause:
                mixer.music.pause()
            else:
                mixer.music.unpause()
        elif self._play_rect.collidepoint(*mouse.get_pos()):
            self._field.shuffle_cards()

    def render(self, screen: surface.Surface) -> None:
        """ Renders in-class objects. """

        screen.blit(self._background, (0, 0))

        screen.blit(self._sound, self._sound_rect)
        screen.blit(self._play, self._play_rect)

        if self._is_pause:
            screen.blit(self._null, self._sound_rect)

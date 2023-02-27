import ctypes


def set_title_bar_color(hwnd: int, *, _value: int = 2) -> None:  # contains unused tools
    """ Recolors the window title to black. """

    value = ctypes.c_int(_value)

    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        ctypes.windll.user32.GetParent(hwnd), 20, ctypes.byref(value), ctypes.sizeof(value)
    )

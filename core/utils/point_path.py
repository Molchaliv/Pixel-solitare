from pygame import rect


def point_path(x_0: int, y_0: int, x_1: int, y_1: int, *, between: int = -1, speed: int = 1) -> list[tuple[int, int]]:  # contains unused tools
    """ Creates a list with intermediate coordinates between start and end for animation projection. """

    x_path = abs(x_1 - x_0)
    y_path = abs(y_1 - y_0)
    if between == -1 and x_path >= y_path:
        between = x_path
    elif between == -1 and y_path >= x_path:
        between = y_path

    x_spacing = (x_1 - x_0) / (between + 1)
    y_spacing = (y_1 - y_0) / (between + 1)

    output = []
    for chunk in [(round(x_0 + index * x_spacing), round(y_0 + index * y_spacing)) for index in range(1, between + 1)]:  # contains unused tools
        for _ in range(speed):
            output.append(chunk)

    return output


def rect_path(start: rect.Rect, end: rect.Rect, *, between: int = -1) -> list[tuple[int, int]]:
    """ Creates a list with intermediate coordinates between start and end for animation projection. """

    return point_path(start.x, start.y, end.x, end.y, between=between)

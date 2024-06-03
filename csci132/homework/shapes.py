# jezzy jumble
# 2024-05-05
# CSCI132 Assigment:  Draw Shapes

"""Draw shapes using turtle.py."""

import turtle as t


def setup(
    width: int,
    height: int,
    title: str,
    background_color: str,
    speed: str = "fast",
    hide: bool = True,
) -> None:
    """Set window options for turtle.

    :param width: width of window in pixels
    :param height: height of window in pixels
    :param title: window name
    :param background_color: background color of window
    :param speed: drawing speed
    :param hide: is turtle cursor hidden?
    """
    t.setup(width=width, height=height, startx=None, starty=None)
    t.title(title)
    t.bgcolor(background_color)
    t.speed(speed)
    if hide:
        t.hideturtle()


def draw_hexagon(x_pos: int, y_pos: int, size: int, color: str) -> None:
    """Draw a filled hexagon with supplied location, size and color.

    :param x_pos: starting absolute x position
    :param y_pos: starting absolute y position
    :param size: length of each side in pixels
    :param color: fill color
    """
    t.teleport(x_pos, y_pos)
    t.fillcolor(color)

    t.begin_fill()
    for _i in range(6):
        t.forward(size)
        t.right(60)  # 360/6 = 60
    t.end_fill()


def draw_octagon(x_pos: int, y_pos: int, size: int, color: str) -> None:
    """Draw a filled octagon with supplied location, size and color.

    :param x_pos: starting absolute x position
    :param y_pos: starting absolute y position
    :param size: length of each side in pixels
    :param color: fill color
    """
    t.teleport(x_pos, y_pos)
    t.fillcolor(color)

    t.begin_fill()
    for _i in range(8):
        t.forward(size)
        t.right(45)  # 360/8 = 45
    t.end_fill()


def draw_triangle(x_pos: int, y_pos: int, size: int, color: str) -> None:
    """Draw a filled equilateral triangle with supplied location, size and color.

    :param x_pos: starting absolute x position
    :param y_pos: starting absolute y position
    :param size: length of each side in pixels
    :param color: fill color
    """
    t.teleport(x_pos, y_pos)
    t.fillcolor(color)

    t.begin_fill()
    for _i in range(3):
        t.forward(size)
        t.left(120)  # 360/3 = 120
    t.end_fill()


def main() -> None:
    """Apply window settings and draw shapes with teacher-provided values."""
    setup(400, 400, "Shapes", "indigo")
    draw_hexagon(80, 150, 40, "yellow")
    draw_octagon(-20, 50, 30, "light green")
    draw_triangle(80, -120, 70, "pink")
    t.exitonclick()  # enter mainloop, and let window be closed with a left mouse click


if __name__ == "__main__":
    main()

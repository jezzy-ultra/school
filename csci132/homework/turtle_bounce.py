# jezzy jumble
# 2024-05-09
# CSCI132 Assigment:  Turtle Bounce

"""Display a turtle trying in vain to escape the window!"""

from random import randint
from tkinter import TclError
from turtle import RawTurtle, Screen

FULL_ROTATION_IN_DEGREES = 360

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_TITLE = "Turtle Bounce!"
WINDOW_BACKGROUND_IMAGE_PATH = "./resources/turtle_bounce_background.png"
WINDOW_BACKGROUND_COLOR = "#b5b5b5"

TURTLE_STRETCH_FACTOR = 2
TURTLE_OUTLINE_FACTOR = 1.5
TURTLE_MOVE_SPEED_IN_PIXELS = 5
TURTLE_FILL_COLOR = "#ff8fa3"
TURTLE_SIZE = TURTLE_STRETCH_FACTOR * 20  # default turtle size is 20x20 pixels

BUFFER_SIZE = 10


def setup(screen: Screen, turtle: RawTurtle) -> None:
    """Set up window and turtle state.

    :param screen: the window
    :param turtle: turtle object
    """
    screen.mode("logo")
    screen.setup(WINDOW_WIDTH, WINDOW_HEIGHT, startx=None, starty=None)
    screen.title(WINDOW_TITLE)
    screen.bgpic(WINDOW_BACKGROUND_IMAGE_PATH)
    screen.bgcolor(WINDOW_BACKGROUND_COLOR)

    turtle.penup()
    turtle.shape("turtle")
    turtle.fillcolor(TURTLE_FILL_COLOR)
    turtle.resizemode("user")  # resize turtle using stretch factor and outline width
    turtle.turtlesize(
        stretch_wid=TURTLE_STRETCH_FACTOR,
        stretch_len=TURTLE_STRETCH_FACTOR,
        outline=TURTLE_OUTLINE_FACTOR,
    )
    turtle.setundobuffer(BUFFER_SIZE)


def is_turtle_off_screen(turtle: RawTurtle) -> bool:
    """Calculate if the turtle's position exceeds the window's boundaries.

    :param turtle: turtle object
    :return: true if the turtle is completely off-screen
    """
    x, y = turtle.position()
    return bool(
        x + TURTLE_SIZE / 2 < -(WINDOW_WIDTH / 2)
        or x - TURTLE_SIZE / 2 > WINDOW_WIDTH / 2
        or y + TURTLE_SIZE / 2 < (-WINDOW_HEIGHT / 2)
        or y - TURTLE_SIZE / 2 > WINDOW_HEIGHT / 2
    )


def move(turtle: RawTurtle) -> None:
    """Move the turtle in a random direction.

    If the turtle is off-screen, place it back on-screen moving in a new direction.

    :param turtle: turtle object
    """
    while True:
        direction = randint(0, FULL_ROTATION_IN_DEGREES)
        turtle.setheading(direction)

        while not is_turtle_off_screen(turtle):
            turtle.forward(TURTLE_MOVE_SPEED_IN_PIXELS)
        # move turtle back onto screen
        while turtle.undobufferentries():
            turtle.undo()


def main() -> None:
    """Set up the window and move the turtle around in it."""
    screen = Screen()
    turtle = RawTurtle(screen)
    setup(screen, turtle)

    # hide error when closing window
    try:
        move(turtle)
        screen.mainloop()
    except TclError:
        pass


if __name__ == "__main__":
    main()

# jezzy jumble
# 2024-05-19
# CSCI132 Assignment:  Balls Bounce

"""Display balls bouncing around a window!"""

import contextlib
import time
from random import randint
from tkinter import TclError
from turtle import RawTurtle, Screen

FRAMES_PER_SECOND = 144
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_TITLE = "Balls Bounce!"
WINDOW_BACKGROUND_COLOR = "#b5b5b5"

NUM_BALLS = 5
BALL_MOVE_SPEED_IN_PIXELS = 5
BALL_FILL_COLOR = "red"
# default turtle object size is 20x20 pixels
BALL_STRETCH_FACTOR = 2
# default ball outline width is 1 pixel
BALL_OUTLINE_FACTOR = 2
BALL_SIZE = (BALL_STRETCH_FACTOR * 20) + BALL_OUTLINE_FACTOR


def create_window() -> Screen:
    """Set up window state.

    :return: the window object
    """
    screen = Screen()
    screen.title(WINDOW_TITLE)
    screen.bgcolor(WINDOW_BACKGROUND_COLOR)
    # fudge window size to account for window borders and titlebar
    screen.setup(WINDOW_WIDTH + 2, WINDOW_HEIGHT + 4)
    screen.screensize(WINDOW_WIDTH, WINDOW_HEIGHT)
    # turn off automatic screen updates
    screen.tracer(0)

    return screen


def create_balls(screen: Screen) -> list[RawTurtle]:
    """Return a list of ball-shaped turtle objects.

    :param screen: the window object
    :return: the list of balls
    """
    balls = []
    for _ in range(NUM_BALLS):
        ball = RawTurtle(
            screen,
            shape="circle",
        )
        ball.penup()
        # resize ball using stretch factor and outline width
        ball.resizemode("user")
        ball.fillcolor(BALL_FILL_COLOR)
        ball.turtlesize(
            stretch_wid=BALL_STRETCH_FACTOR,
            stretch_len=BALL_STRETCH_FACTOR,
            outline=BALL_OUTLINE_FACTOR,
        )
        ball.setheading(randint(0, 360))

        balls.append(ball)

    return balls


def is_ball_off_screen(ball: RawTurtle) -> bool:
    """Calculate if a ball's position exceeds the window's boundaries.

    :param ball: a turtle object
    :return: true if the ball is completely off-screen
    """
    x, y = ball.position()
    turtle_radius = BALL_SIZE / 2
    screen_left_boundary = -(WINDOW_WIDTH / 2)
    screen_top_boundary = WINDOW_HEIGHT / 2
    # fudge boundary checks for better collision detection
    screen_right_boundary = (WINDOW_WIDTH / 2) - 10
    screen_bottom_boundary = -(WINDOW_WIDTH / 2) + 8

    return bool(
        (x - turtle_radius) <= screen_left_boundary
        or (y + turtle_radius) >= screen_top_boundary
        or (x + turtle_radius) >= screen_right_boundary
        or (y - turtle_radius) <= screen_bottom_boundary
    )


def move_balls_randomly_loop(screen: Screen, balls: list[RawTurtle]) -> None:
    """Bounce the balls around and keep them in bounds.

    This function acts as the loop for our program;
    once its called it runs until the user closes the window.
    The frame rate is limited to the value set by FRAMES_PER_SECOND.

    :param screen: the window object
    :param balls: the list of turtle objects
    """
    frame_time = 1.0 / FRAMES_PER_SECOND
    while True:
        start_time = time.time()

        for ball in balls:
            if is_ball_off_screen(ball):
                ball.undo()
                # keep in range: [0, 360]
                opposite_direction = (ball.heading() + 180) % 360
                # vary new angle slightly
                random_direction = (opposite_direction + randint(-45, 45)) % 360
                ball.setheading(random_direction)
            else:
                ball.forward(BALL_MOVE_SPEED_IN_PIXELS)
        screen.update()

        end_time = time.time()
        frame_duration = end_time - start_time
        if frame_duration < frame_time:
            time.sleep(frame_time - frame_duration)


def main() -> None:
    """Set up the window and bounce balls around in it."""
    screen = create_window()
    balls = create_balls(screen)

    # hide error when closing window
    with contextlib.suppress(TclError, KeyboardInterrupt):
        move_balls_randomly_loop(screen, balls)


if __name__ == "__main__":
    main()

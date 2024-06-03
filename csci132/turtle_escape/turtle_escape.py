"""A game about getting your turtle to the end while dodging enemies.

Move your turtle friend to your friend at the other end of the screen with the arrow
or WASD keys and dodge the bouncing balls along the way. They can't go through the
dashed lines but you can! The levels get progressively harder.

:Author: jezzy jumble
:Date: 2024-06-02
:Assignment: Turtle Escape (CSCI 132)
"""

import contextlib
import enum
import math
import random
import time
import turtle
from dataclasses import dataclass
from tkinter import TclError
from turtle import RawTurtle, Screen


class GameState(enum.Enum):
    """The current state of the game and track how the player is doing."""

    PLAYING = enum.auto()
    CLEARED_LEVEL = enum.auto()
    GAME_OVER = enum.auto()
    WON = enum.auto()
    QUITTING = enum.auto()
    RESTARTING = enum.auto()


class ScreenCorner(enum.Enum):
    """The four corners of the window."""

    TOP_LEFT = enum.auto()
    TOP_RIGHT = enum.auto()
    BOTTOM_LEFT = enum.auto()
    BOTTOM_RIGHT = enum.auto()


class EnemyStartingSide(enum.StrEnum):
    """The side of the screen an enemy starts on."""

    LEFT = enum.auto()
    RIGHT = enum.auto()


@dataclass
class LevelInfo:
    """The properties of a level."""

    num_walls: int
    num_wall_pieces: int
    enemy_move_speed: float


@dataclass
class Player:
    """The turtle controlled by the player."""

    entity: RawTurtle
    radius: float


@dataclass
class Goal:
    """The turtle that the player is trying to reach."""

    entity: RawTurtle
    radius: float


@dataclass
class WallYBounds:
    """The y-coordinates of the current level's walls."""

    bottom: float
    top: float


@dataclass
class WallGapBounds:
    """The x-coordinates of a wall's gap, and its wall's y-coordinate."""

    y_coord: float
    left_x_coord: float
    right_x_coord: float


@dataclass
class WallGenerator:
    """The object responsible for generating the level's walls."""

    entity: RawTurtle
    y_bounds_list: list[WallYBounds]
    gap_bounds_list: list[WallGapBounds]


@dataclass
class Enemy:
    """A bouncing ball the player is trying to avoid."""

    entity: RawTurtle
    radius: float
    x_velocity: float
    y_velocity: float
    wall_y_bounds: WallYBounds
    starting_side: EnemyStartingSide


LEVELS = {
    1: LevelInfo(num_walls=2, num_wall_pieces=2, enemy_move_speed=2.5),
    2: LevelInfo(num_walls=3, num_wall_pieces=2, enemy_move_speed=3),
    3: LevelInfo(num_walls=4, num_wall_pieces=3, enemy_move_speed=3),
    4: LevelInfo(num_walls=5, num_wall_pieces=3, enemy_move_speed=4),
    5: LevelInfo(num_walls=6, num_wall_pieces=4, enemy_move_speed=4),
}

MSG_WON = "You saved your little turtle friends!"
MSG_GAME_OVER = "You're turtle soup!"
MSG_INVALID_INPUT = "Sorry, I didn't quite catch that."
MSG_PLAY_AGAIN = "Play again? [Y/n]"
ERROR_MSG_INVALID_GAME_STATE = "invalid `GameState` value"
ERROR_MSG_WALL_VALUES_TOO_LOW = (
    "both `num_walls` and `num_wall_pieces` must have a value of at least 2"
)

FRAME_TIME = 1.0 / 144  # frames per second
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# fudge boundaries
SCREEN_LEFT_BOUNDARY = -(WINDOW_WIDTH / 2)
SCREEN_TOP_BOUNDARY = WINDOW_HEIGHT / 2
SCREEN_RIGHT_BOUNDARY = WINDOW_WIDTH / 2
SCREEN_BOTTOM_BOUNDARY = -(WINDOW_HEIGHT / 2)

# default turtle shape size is 20x20 pixels
STAMP_SIZE = 21
PLAYER_MOVE_SPEED = 25  # in pixels

game_state = GameState.PLAYING
current_level = 1
screen = Screen()
player = Player(RawTurtle(screen), 0)
goal = Goal(RawTurtle(screen), 0)
wall_generator = WallGenerator(RawTurtle(screen), [], [])
enemies: list[Enemy] = []


def game_loop() -> None:
    """Loop the game logic until the player wins or loses."""
    global game_state
    global current_level

    current_level = 1
    while True:
        game_state = GameState.PLAYING

        screen.clear()
        set_up_screen()
        set_up_player()
        set_up_goal()
        set_up_walls()
        set_up_enemies()

        set_up_screen_inputs()

        while game_state == GameState.PLAYING:
            start_time = time.time()

            check_player_collisions()
            move_enemies()
            check_enemy_collisions()

            if game_state == GameState.CLEARED_LEVEL:
                current_level += 1
                if current_level not in LEVELS:
                    game_state = GameState.WON
                else:
                    game_state = GameState.PLAYING
                    break

            if game_state in {GameState.WON, GameState.GAME_OVER}:
                restart_or_quit()
                if game_state == GameState.RESTARTING:
                    current_level = 1
                    screen.clear()
                    break
                screen.bye()

            screen.update()

            end_time = time.time()
            delta_time = end_time - start_time
            if delta_time < FRAME_TIME:
                time.sleep(FRAME_TIME - delta_time)


def set_up_screen() -> None:
    """Set up the window and the properties of the game's screen."""
    global screen

    screen = Screen()
    screen.title("Turtle Escape")
    screen.mode()
    screen.bgcolor("white")
    # fudge window size to account for window borders and titlebar
    screen.setup(WINDOW_WIDTH + 2, WINDOW_HEIGHT + 4)
    screen.screensize(WINDOW_WIDTH, WINDOW_HEIGHT)
    # turn off automatic screen updates; update in batches for performance
    screen.tracer(0)


def set_up_screen_inputs() -> None:
    """Listen for player input (arrow and WASD keys)."""
    screen.onkeypress(move_player_up, "Up")
    screen.onkeypress(move_player_up, "w")
    screen.onkeypress(move_player_right, "Right")
    screen.onkeypress(move_player_right, "d")
    screen.onkeypress(move_player_down, "Down")
    screen.onkeypress(move_player_down, "s")
    screen.onkeypress(move_player_left, "Left")
    screen.onkeypress(move_player_left, "a")
    screen.listen()


def move_player_up() -> None:
    """Move the player turtle upwards."""
    player.entity.goto(player.entity.xcor(), player.entity.ycor() + PLAYER_MOVE_SPEED)


def move_player_right() -> None:
    """Move the player turtle right."""
    player.entity.goto(player.entity.xcor() + PLAYER_MOVE_SPEED, player.entity.ycor())


def move_player_down() -> None:
    """Move the player turtle downwards."""
    player.entity.goto(player.entity.xcor(), player.entity.ycor() - PLAYER_MOVE_SPEED)


def move_player_left() -> None:
    """Move the player turtle left."""
    player.entity.goto(player.entity.xcor() - PLAYER_MOVE_SPEED, player.entity.ycor())


def set_up_player() -> None:
    """Set up the player turtle object."""
    global player

    player_entity = RawTurtle(screen)
    player_entity.penup()
    player_entity.shape("turtle")
    player_entity.fillcolor("light pink")
    player_entity.resizemode(
        "user"
    )  # resize player using stretch factor and outline width
    player_entity.turtlesize(
        stretch_wid=1.5,
        stretch_len=1.5,
        outline=2,
    )
    player_radius = calculate_entity_radius(player_entity)

    player = Player(player_entity, player_radius)
    teleport_entity(player, ScreenCorner.BOTTOM_RIGHT)


def set_up_goal() -> None:
    """Set up the goal turtle object."""
    global goal

    goal_entity = RawTurtle(screen)
    goal_entity.penup()
    goal_entity.shape("turtle")
    goal_entity.fillcolor("blue")
    goal_entity.resizemode("user")  # resize goal using stretch factor and outline width
    goal_entity.turtlesize(
        stretch_wid=2,
        stretch_len=2,
        outline=1.5,
    )
    goal_radius = calculate_entity_radius(goal_entity)

    goal = Goal(goal_entity, goal_radius)
    teleport_entity(goal, ScreenCorner.TOP_LEFT)


def calculate_entity_radius(entity: RawTurtle) -> float:
    """Calculate the radius of the player, goal, or an enemy.

    :param entity: a turtle object
    :return: the entity's radius
    """
    width = entity.turtlesize()[0]
    height = entity.turtlesize()[1]
    outline_thickness = entity.turtlesize()[2]
    diameter = math.sqrt(width**2 + height**2)

    return (diameter / 2) + outline_thickness


def teleport_entity(
    entity: Player | Goal | Enemy, location: tuple[float, float] | ScreenCorner
) -> None:
    """Move the player, goal, or an enemy instantaneously to a desired position.

    :param entity: a turtle object
    :param location: the corner of a screen, or arbitrary (x, y) coordinates
    """
    match location:
        case ScreenCorner.TOP_LEFT:
            x_coord = SCREEN_LEFT_BOUNDARY + entity.radius**3
            y_coord = SCREEN_TOP_BOUNDARY - entity.radius**3
            direction = 270  # south
        case ScreenCorner.TOP_RIGHT:
            x_coord = SCREEN_RIGHT_BOUNDARY - entity.radius**3
            y_coord = SCREEN_TOP_BOUNDARY - entity.radius**3
            direction = 270  # south
        case ScreenCorner.BOTTOM_LEFT:
            x_coord = SCREEN_LEFT_BOUNDARY + entity.radius**3
            y_coord = SCREEN_BOTTOM_BOUNDARY + entity.radius**3
            direction = 90  # north
        case ScreenCorner.BOTTOM_RIGHT:
            x_coord = SCREEN_RIGHT_BOUNDARY - entity.radius**3
            y_coord = SCREEN_BOTTOM_BOUNDARY + entity.radius**3
            direction = 90  # north
        case _:
            x_coord = location[0]
            y_coord = location[1]
            direction = None

    entity.entity.teleport(x_coord, y_coord)
    if direction is not None:
        entity.entity.setheading(direction)


def set_up_walls() -> None:
    """Generate the level's walls, each with a randomly placed gap."""
    global wall_generator

    level = LEVELS[current_level]

    if level.num_walls < 2 or level.num_wall_pieces < 2:
        raise ValueError(ERROR_MSG_WALL_VALUES_TOO_LOW)

    generator = RawTurtle(screen)
    generator.hideturtle()
    generator.setheading(0)  # east
    generator.pensize(4)

    gap_height = WINDOW_HEIGHT / (level.num_walls + 1)
    wall_piece_width = WINDOW_WIDTH / level.num_wall_pieces

    dash_length = 5
    num_dashes = int(wall_piece_width / (2 * dash_length))

    gap_x_coords: list[tuple[float, float]] = []
    y_coords: list[float] = []
    last_gap_piece = 0
    for i in range(level.num_walls):
        gap_piece = 0
        while gap_piece in {0, last_gap_piece}:
            gap_piece = random.randint(1, level.num_wall_pieces)
        last_gap_piece = gap_piece

        num_left_pieces = gap_piece - 1
        num_right_pieces = (level.num_wall_pieces - num_left_pieces) - 1

        generator.teleport(
            SCREEN_LEFT_BOUNDARY,
            SCREEN_BOTTOM_BOUNDARY + (gap_height * (i + 1)),
        )
        y_coords.append(generator.ycor())

        generator.pencolor("black")
        generator.pendown()
        generator.forward(num_left_pieces * wall_piece_width)

        generator.pencolor("light gray")
        gap_left_x_coord = generator.xcor()
        for _ in range(num_dashes):
            generator.pendown()
            generator.forward(dash_length)
            generator.penup()
            generator.forward(dash_length)
        gap_right_x_coord = generator.xcor()
        gap_x_coords.append((gap_left_x_coord, gap_right_x_coord))

        generator.pencolor("black")
        generator.pendown()
        generator.forward(num_right_pieces * wall_piece_width)

    wall_y_bounds_list, wall_gap_bounds_list = create_wall_bounds_lists(
        y_coords, gap_x_coords
    )
    wall_generator = WallGenerator(generator, wall_y_bounds_list, wall_gap_bounds_list)


def create_wall_bounds_lists(
    y_coords: list[float], gap_x_coords: list[tuple[float, float]]
) -> tuple[list[WallYBounds], list[WallGapBounds]]:
    """Create the lists of bounds objects using the level's wall coordinates.

    :param y_coords: list of each wall's y-coordinate in the level
    :param gap_x_coords: list of each wall gap's x-coordinates in the level
    :return the wall bounds objects
    """
    wall_y_bounds_list = []
    wall_gap_bounds_list = []
    for i, y_coord in enumerate(y_coords):
        wall_gap_bounds = WallGapBounds(
            y_coord, left_x_coord=gap_x_coords[i][0], right_x_coord=gap_x_coords[i][1]
        )
        wall_gap_bounds_list.append(wall_gap_bounds)

        try:
            next_y_coord = y_coords[i + 1]
            wall_y_bounds = WallYBounds(y_coord, next_y_coord)

            wall_y_bounds_list.append(wall_y_bounds)

        except IndexError:
            continue

    return wall_y_bounds_list, wall_gap_bounds_list


def set_up_enemies() -> None:
    """Populate the level with enemies."""
    global enemies

    enemies = []
    is_left = bool(random.randint(0, 1))
    for wall_y_bounds in wall_generator.y_bounds_list:
        starting_side = EnemyStartingSide.LEFT if is_left else EnemyStartingSide.RIGHT
        is_left = not is_left

        enemies.append(generate_enemy(wall_y_bounds, starting_side))

    teleport_enemies()


def generate_enemy(
    wall_y_bounds: WallYBounds, starting_side: EnemyStartingSide
) -> Enemy:
    """Generate an enemy bound between a set of walls.

    :param wall_y_bounds: a pair of adjacent walls' y-coordinates
    :param starting_side: the side of the screen to place the enemy on initially
    :return an enemy object
    """
    enemy_entity = RawTurtle(
        screen,
        shape="circle",
    )
    enemy_entity.penup()
    enemy_entity.fillcolor("red")
    enemy_entity.resizemode(
        "user"
    )  # resize enemy using stretch factor and outline width
    enemy_entity.turtlesize(
        stretch_wid=2,
        stretch_len=2,
        outline=2,
    )

    enemy_radius = calculate_entity_radius(enemy_entity)
    speed = LEVELS[current_level].enemy_move_speed
    x_velocity = speed if starting_side == EnemyStartingSide.LEFT else -speed
    y_velocity = random.random() * speed
    if random.randint(0, 1):
        y_velocity *= -1

    return Enemy(
        enemy_entity, enemy_radius, x_velocity, y_velocity, wall_y_bounds, starting_side
    )


def teleport_enemies() -> None:
    """Move the level's enemies to their appropriate positions."""
    for enemy in enemies:
        # center enemy y-coordinate
        y_coord = (
            float(enemy.wall_y_bounds.top) + float(enemy.wall_y_bounds.bottom)
        ) / 2
        if enemy.starting_side == EnemyStartingSide.LEFT:
            x_coord = SCREEN_LEFT_BOUNDARY + 10 + (enemy.radius**2 * 2.5)
        else:
            x_coord = SCREEN_RIGHT_BOUNDARY - (10 + (enemy.radius**2 * 2.5))

        enemy.entity.teleport(x_coord, y_coord)


def check_player_collisions() -> None:
    """Check if the player has reached the goal or exceeded a wall or screen boundary.

    If they've reached the goal turtle, set the level as cleared. If they've collided
    with a wall or boundary, prevent them from going further in that direction.
    """
    global game_state

    if have_entities_collided(player, goal):
        game_state = GameState.CLEARED_LEVEL

    if (
        has_entity_hit_screen_horizontal_boundary(player)
        or has_player_hit_screen_vertical_boundary()
        or has_player_hit_wall()
    ):
        player.entity.undo()


def have_entities_collided(
    entity1: Player | Goal | Enemy, entity2: Player | Goal | Enemy
) -> bool:
    """Check if two game entities have collided.

    entity1: the player, goal, or an enemy object
    entity2: the player, goal, or an enemy object
    return: true if there's a collision
    """
    # noinspection PyTypeChecker
    return entity1.entity.distance(entity2.entity.pos()) <= (entity1.radius * 4) + (
        entity2.radius * 4
    )


def has_entity_hit_screen_horizontal_boundary(entity: Player | Enemy) -> bool:
    """Calculate if a game entity's position exceeds the window's horizontal boundaries.

    :param entity: a turtle object (player or enemy entity)
    :return: true if the entity is off-screen in the left or right directions
    """
    return bool(
        entity.entity.xcor() - (entity.radius**2 * 2) <= SCREEN_LEFT_BOUNDARY - 6
        or entity.entity.xcor() + (entity.radius**2 * 2) >= SCREEN_RIGHT_BOUNDARY - 6
    )


def has_player_hit_screen_vertical_boundary() -> bool:
    """Calculate if the player's position exceeds the window's vertical boundaries.

    :return: true if the player is off-screen in the up or down directions
    """
    y_coord = player.entity.ycor()

    return bool(
        y_coord + (player.radius**2 * 2) >= SCREEN_TOP_BOUNDARY
        or y_coord - (player.radius**2 * 2) <= SCREEN_BOTTOM_BOUNDARY
    )


def has_player_hit_wall() -> bool:
    """Check if the player has collided with a wall.

    return: true if there's a collision
    """
    for wall_gap_bounds in wall_generator.gap_bounds_list:
        if wall_gap_bounds.y_coord - (
            player.radius * 5
        ) <= player.entity.ycor() <= wall_gap_bounds.y_coord + (
            player.radius * 5
        ) and not wall_gap_bounds.left_x_coord + (
            player.radius * 3
        ) <= player.entity.xcor() <= wall_gap_bounds.right_x_coord - (
            player.radius * 3
        ):
            return True
    return False


def move_enemies() -> None:
    """Move each enemy in the level by their current velocities."""
    for enemy in enemies:
        enemy.entity.goto(
            enemy.entity.xcor() + enemy.x_velocity,
            enemy.entity.ycor() + enemy.y_velocity,
        )


def check_enemy_collisions() -> None:
    """Check if the enemies in the level have collided with the player or a boundary.

    If an enemy has hit the player, the game is over. If an enemy has hit a wall or
    screen boundary, bounce them off of it.
    """
    global game_state

    for enemy in enemies:
        if have_entities_collided(player, enemy) and game_state not in {
            GameState.CLEARED_LEVEL,
            GameState.WON,
        }:
            game_state = GameState.GAME_OVER
            break

        if has_entity_hit_screen_horizontal_boundary(enemy):
            enemy.x_velocity *= -1
        if has_enemy_hit_wall(enemy):
            enemy.y_velocity *= -1


def has_enemy_hit_wall(enemy: Enemy) -> bool:
    """Check if an enemy has collided with a wall.

    :param enemy: an enemy object
    :return true if there's a collision
    """
    return bool(
        not enemy.wall_y_bounds.bottom + (enemy.radius**2 * 2)
        <= enemy.entity.ycor()
        <= enemy.wall_y_bounds.top - (enemy.radius**2 * 2)
    )


def restart_or_quit() -> None:
    """Display a dialog and ask the player if they want to restart the game or quit.

    This gets triggered when the player either wins or loses the game.
    """
    global game_state

    if game_state == GameState.WON:
        title = "WINNER!"
        msg = f"{MSG_WON} {MSG_PLAY_AGAIN}"
    elif game_state == GameState.GAME_OVER:
        title = "GAME OVER"
        msg = f"{MSG_GAME_OVER} {MSG_PLAY_AGAIN}"
    else:
        raise ValueError(ERROR_MSG_INVALID_GAME_STATE)

    try:
        play_again_input = screen.textinput(title, msg).lower()
        while play_again_input not in {"", "y", "yes", "n", "no"}:
            play_again_input = screen.textinput(
                title, f"Sorry, didn't catch that.\n{MSG_PLAY_AGAIN}"
            ).lower()
        if not play_again_input or play_again_input[0] == "y":
            game_state = GameState.RESTARTING
        else:
            game_state = GameState.QUITTING
    except AttributeError:
        screen.bye()


def main() -> None:
    """Start the game loop and hide random errors when the player closes the window."""
    # hide errors when user closes window
    with contextlib.suppress(TclError, KeyboardInterrupt, turtle.Terminator):
        game_loop()
        screen.mainloop()


if __name__ == "__main__":
    main()

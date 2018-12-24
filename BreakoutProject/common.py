import math
from enum import Enum
from collections import namedtuple

Size = namedtuple('Size', ['width', 'height'])

# CONSTANTS
BALL_SIZE = Size(35, 35)
SHIP_SIZE = Size(200, 25)
BONUS_SIZE = Size(25, 25)
BRICK_SIZE = Size(100, 20)
BULLET_SIZE = Size(10, 20)

BALL_VELOCITY = 13
SHIP_VELOCITY = 17
BONUS_VELOCITY = 10
BULLET_VELOCITY = 13

BALL_DIRECTION = (-1, 1)
SHIP_DIRECTION = (0, 0)
BONUS_DIRECTION = (0, 1)
BULLET_DIRECTION = (0, -1)


class BallState(Enum):
    Caught = 0
    Free = 1
    Powerful = 2


def compare(one, other):
    """function compares two numbers
    return value: -1 (one < other)
                  +1 (one > other)"""
    if one < other:
        return -1
    else:
        return int(one > other)


def sign(number):
    """Function returns sign of number"""
    if number == 0:
        return number
    return int(math.copysign(1, number))

import math
from enum import Enum
from collections import namedtuple

Size = namedtuple('Size', ['width', 'height'])

# CONSTANTS
BALL_SIZE = Size(35, 35)
PADDLE_SIZE = Size(200, 25)
BONUS_SIZE = Size(35, 35)
BRICK_SIZE = Size(100, 35)

BALL_VELOCITY = 12
PADDLE_VELOCITY = 25
BONUS_VELOCITY = 10

BALL_DIRECTION = (-1, 1)
PADDLE_DIRECTION = (0, 0)
BONUS_DIRECTION = (0, 1)


class BallState(Enum):
    Caught = 0
    Free = 1
    Powerful = 2


class Bonuses(Enum):
    DecreaseBonus = 0
    ExpandBonus = 1
    FireBallBonus = 2
    FastBallBonus = 3
    LifeBonus = 4
    DeathBonus = 5


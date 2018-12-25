import random
import common
from math import pi, cos

from abstract_objects import BonusObject
from moving_objects import Ball, Paddle
from base import Frame, Vector
from levels import LevelCreator


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0
        self.lives = 3              # videti da li da bude static ili kako vec

    def gain_life(self):
        self.lives += 1

    def lose_life(self):
        self.lives -= 1

    def get_score(self, brick_count):
        self.score += 10 * brick_count


class Game:
    """TREBACE DVA PADDLE-a, DVA IGRACA, itd....."""
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.player1 = Player(1)
        self.player2 = Player(2)
        self.current_level = 1
        self.won = False
        self.reset()
        self.stop_height = self.paddle.bottom - self.paddle.frame.height / 2

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

        self.bonuses = set()

    @property
    def game_over(self):
        return self.player1.lives == 0 or self.player2.lives == 0

    @property
    def level_completed(self):
        return len(self.level.blocks) == 0

    def get_objects(self):
        yield self.paddle
        yield self.ball

        for block in self.level.blocks:
            yield block
        for bonus in self.bonuses:
            yield bonus

    def release_ball(self):
        if self.ball.state == common.BallState.Caught:
            self.ball.change_state(common.BallState.Free)
            return True
        return False

    def try_get_next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels) +1
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def reset(self):
        self.bonuses = set()
        self.paddle = Paddle((self.size.width - common.SHIP_SIZE.width) / 2, self.size.height - common.SHIP_SIZE.height)
        ball_x = self.paddle.x + (self.paddle.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_ship()

    def kill_player(self):
        self.player1.lose_life()
        self.player2.lose_life()
        self.reset()
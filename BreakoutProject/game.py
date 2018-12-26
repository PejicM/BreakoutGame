import random
import common
from math import pi, cos

from abstract_objects import BonusObject
from moving_objects import Ball, Paddle
from base import Frame, Vector
from levels import LevelCreator


class Player:
    lives = 3       # static field

    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0

    def gain_life(self):
        self.lives += 1

    def lose_life(self):
        self.lives -= 1

    def get_score(self, brick_count):
        self.score += 10 * brick_count


class GameTwoPlayers:
    """TREBACE DVA PADDLE-a, DVA IGRACA, itd....."""
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.player1 = Player(1)
        self.player2 = Player(2)
        self.current_level = 1
        self.won = False
        self.reset()
        self.border_line = self.paddle1.bottom - self.paddle1.frame.height / 2        # granicka linija ispod koje loptica ne sme pasti

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

        self.bonuses = set()

    @property
    def game_over(self):
        return Player.lives == 0

    @property
    def level_completed(self):
        return len(self.level.blocks) == 0

    def get_objects(self):
        yield self.paddle1
        yield self.paddle2
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
        if self.current_level < len(self.levels) + 1:
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def tick(self, turn_rate=0):
        pass

    def reset(self):
        self.bonuses = set()
        self.paddle1 = Paddle((self.size.width - common.PADDLE_SIZE.width) / 2, self.size.height - common.PADDLE_SIZE.height)
        self.paddle2 = Paddle((self.size.width - common.PADDLE_SIZE.width) / 4, self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle1.x + (self.paddle1.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle1.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_ship()

    def kill_player(self):
        self.player1.lose_life()
        self.player2.lose_life()
        self.reset()


class GameOnePlayer:
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.player = Player(1)
        self.current_level = 1
        self.won = False
        self.reset()
        self.border_line = self.paddle.bottom - self.paddle.frame.height / 2        # granicka linija ispod koje loptica ne sme pasti

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

        self.bonuses = set()

    @property
    def game_over(self):
        return self.player.lives == 0

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
        if self.current_level < len(self.levels) + 1:
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def tick(self, turn_rate=0):
        pass

    def reset(self):
        self.bonuses = set()
        self.paddle = Paddle((self.size.width - common.PADDLE_SIZE.width) / 2, self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle.x + (self.paddle.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_ship()

    def kill_player(self):
        self.player.lose_life()
        self.reset()

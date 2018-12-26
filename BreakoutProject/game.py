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

    def get_next_level(self):
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
        self.paddle1 = Paddle(1, (self.size.width - common.PADDLE_SIZE.width) * 0.25, self.size.height - common.PADDLE_SIZE.height)
        self.paddle2 = Paddle(2, (self.size.width - common.PADDLE_SIZE.width) * 0.75, self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle1.x + (self.paddle1.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle1.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_paddle()

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

    def reset(self):
        self.bonuses = set()
        self.paddle = Paddle(1, (self.size.width - common.PADDLE_SIZE.width) / 2, self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle.x + (self.paddle.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.stick_to_paddle()

    def release_ball(self):
        if self.ball.state == common.BallState.Caught:
            self.ball.change_state(common.BallState.Free)
            return True
        return False

    def get_next_level(self):
        self.current_level += 1
        if self.current_level < len(self.levels) + 1:
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def tick(self, turn_rate=0):
        """ Promene polozaja objekata na svaki otkucaj tajmera """
        if self.game_over or self.won:
            return

        old_x = self.paddle.left
        self.paddle.move(turn_rate)
        self.normalize_paddle_location()
        self.ball.move(self.paddle.left - old_x)
        self.reflect_ball()

        if self.ball.middle > self.border_line:
            self.kill_player()

        if self.level_completed:
            self.player.score += 100 * self.current_level
            if not self.get_next_level():
                self.won = True

        blocks_to_remove = {block for block in self.level.blocks
                            if block.intersects_with(self.ball)}
        if len(blocks_to_remove) != 0:
            self.remove_blocks(blocks_to_remove)

        self.remove_bonuses()

        if self.ball.contact_two_frames(self.paddle):
            mid = self.paddle.right - self.paddle.width / 2
            ball_mid = self.ball.right - self.ball.width / 2
            self.ball.direction = Vector.from_angle(
                -pi / 2 + (pi / 2.75 * (ball_mid - mid) /
                           (self.paddle.width / 2)))

    def normalize_paddle_location(self):
        self.paddle.location = (min(max(0, self.paddle.left), self.frame.right - self.paddle.width), self.paddle.y)

    def reflect_ball(self):
        """ Odbijanje lopte, po principu menjanja smera vektora (predzaci x i y koordinate) """
        ball = self.ball

        if (ball.direction.x > 0 and ball.right > self.frame.right) or \
                (ball.direction.x < 0 and ball.x < self.frame.left):
            ball.direction.x = -ball.direction.x

        if ball.direction.y < 0 and ball.y < self.frame.top + 0.1:
            ball.direction.y = -ball.direction.y

    def get_bonus(self, block):
        chance = random.random()
        if chance > 0.5:
            random_bonus = BonusObject.get_random_bonus()
            bonus = random_bonus(block.left, block.top)
            self.bonuses.add(bonus)

    def remove_blocks(self, blocks_to_remove):
        block = next(iter(blocks_to_remove))

        if self.ball.state != common.BallState.Fiery:
            ball = self.ball
            delta = ball.center - block.center
            ball.direction.normalize()

            # odbijanje lopte o blok (promena znaka odgovarajuce koordinate)
            if abs(delta.x) - ball.velocity * abs(cos(ball.direction.x)) <= block.width / 2:
                ball.direction.y = -ball.direction.y
            else:
                ball.direction.x = -ball.direction.x

        self.level.blocks -= blocks_to_remove

    def remove_bonuses(self):
        bonuses_to_remove = {bonus for bonus in self.bonuses
                             if not bonus.contact_two_frames(self)}

        for bonus in self.bonuses:
            bonus.move()
            if bonus.contact_two_frames(self.paddle):
                bonus.activate(self)
                bonuses_to_remove.add(bonus)

        self.bonuses -= bonuses_to_remove

    def kill_player(self):
        self.player.lose_life()
        self.reset()

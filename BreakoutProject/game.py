import random
import common
from math import pi, cos
from multiprocessing import Queue
from PyQt5.QtCore import Qt

from common import BallState
from abstract_objects import BonusObject
from moving_objects import Ball, Paddle
from still_objects import Brick
from base import Frame, Vector
from levels import LevelCreator
from desire_bonuses import ExpandBonus, FireballBonus, LifeBonus
from undesire_bonuses import ShrinkBonus, DeathBonus, FastBallBonus


class Player:
    lives = 3  # static field

    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0
        self.bonuses = set()

    def gain_life(self):
        if self.lives < 3:
            self.lives += 1

    def lose_life(self):
        self.lives -= 1

    def get_score(self, brick_count):
        self.score += 10 * brick_count


class GameTwoPlayers:
    def __init__(self, size):
        self.size = size
        self.frame = Frame(0, 0, *size)

        self.player1 = Player(1)
        self.player2 = Player(2)
        self.paddle_reflect_ball = 1  # indikator koji paddle je odbio loptu i eventualno pogodio neki blok
        self.current_level = 1
        self.won = False
        self.reset()
        self.border_line = self.paddle1.bottom - self.paddle1.frame.height / 2  # granicka linija ispod koje loptica ne sme pasti

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

    @property
    def game_over(self):
        return self.player1.lives == 0 and self.player2.lives == 0

    @property
    def level_completed(self):
        return len(self.level.blocks) == 0

    def get_paddle(self, queue: Queue):
        queue.put(self.paddle1)
        queue.put(self.paddle2)

    def get_ball(self, queue: Queue):
        queue.put(self.ball)

    def get_objects(self):
        yield self.paddle1
        yield self.paddle2
        yield self.ball

        for block in self.level.blocks:
            yield block
        for bonus1 in self.player1.bonuses:
            yield bonus1
        for bonus2 in self.player2.bonuses:
            yield bonus2

    def reset(self):
        self.player1.bonuses = set()
        self.player2.bonuses = set()
        self.paddle1 = Paddle(1, (self.size.width - common.PADDLE_SIZE.width) * 0.25,
                              self.size.height - common.PADDLE_SIZE.height)
        self.paddle2 = Paddle(2, (self.size.width - common.PADDLE_SIZE.width) * 0.75,
                              self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle1.x + (self.paddle1.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle1.top - common.BALL_SIZE.height
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
            self.ball.velocity *= 1.2
            self.level = self.levels[self.current_level]
            self.reset()
            return True
        return False

    def update_moving_objects(self, key):
        if key == Qt.Key_Right:
            self.paddle2.move(1)
            self.normalize_paddle_location()
        elif key == Qt.Key_Left:
            self.paddle2.move(-1)
            self.normalize_paddle_location()

        if key == Qt.Key_D:
            old_x1 = self.paddle1.left
            self.paddle1.move(1)
            self.normalize_paddle_location()
            # pomeranje lopte
            if self.ball.state == BallState.Caught:
                self.ball.move(self.paddle1.left - old_x1)
                self.reflect_ball()
        elif key == Qt.Key_A:
            old_x1 = self.paddle1.left
            self.paddle1.move(-1)
            self.normalize_paddle_location()
            # pomeranje lopte
            if self.ball.state == BallState.Caught:
                self.ball.move(self.paddle1.left - old_x1)
                self.reflect_ball()

    def tick(self, turn_rate1=0, turn_rate2=0):
        """ Promene polozaja objekata na svaki otkucaj tajmera"""
        if self.game_over or self.won:
            return

        # pomeranje paddle-ova
        old_x1 = self.paddle1.left
        # self.paddle1.move(turn_rate1)

        # old_x2 = self.paddle2.left
        # self.paddle2.move(turn_rate2)

        # self.normalize_paddle_location()

        # pomeranje lopte
        self.ball.move(self.paddle1.left - old_x1)
        self.reflect_ball()

        if self.ball.middle > self.border_line:
            self.kill_player()

        if self.level_completed:
            self.player1.score += 100 * self.current_level
            if not self.get_next_level():
                self.won = True

        # detekcija kolizije lopte i bloka
        blocks_to_remove = set()
        for block in self.level.blocks:
            if block.contact_two_frames(self.ball):
                blocks_to_remove.add(block)

        if len(blocks_to_remove) != 0:
            self.remove_blocks(blocks_to_remove)

        self.remove_bonuses()

        # detekcija kolizije lopte i paddle-a, racunanje smera odbijanja lopte
        if self.ball.contact_two_frames(self.paddle1):
            self.paddle_reflect_ball = 1
            mid = self.paddle1.right - self.paddle1.width / 2
            ball_mid = self.ball.right - self.ball.width / 2
            self.ball.direction = Vector.from_angle(-pi / 2 + (pi / 2.75 * (ball_mid - mid) / (self.paddle1.width / 2)))

        if self.ball.contact_two_frames(self.paddle2):
            self.paddle_reflect_ball = 2
            mid = self.paddle2.right - self.paddle2.width / 2
            ball_mid = self.ball.right - self.ball.width / 2
            self.ball.direction = Vector.from_angle(-pi / 2 + (pi / 2.75 * (ball_mid - mid) / (self.paddle2.width / 2)))

    def normalize_paddle_location(self):
        self.paddle1.location = (min(max(0, self.paddle1.left), self.frame.right - self.paddle1.width), self.paddle1.y)
        self.paddle2.location = (min(max(0, self.paddle2.left), self.frame.right - self.paddle2.width), self.paddle2.y)

    def reflect_ball(self):
        """ Odbijanje lopte, po principu menjanja smera vektora (predzaci x i y koordinate) """
        ball = self.ball

        if (ball.direction.x > 0 and ball.right > self.frame.right) or \
                (ball.direction.x < 0 and ball.x < self.frame.left):
            ball.direction.x = -ball.direction.x

        if ball.direction.y < 0 and ball.y < self.frame.top + 0.1:
            ball.direction.y = -ball.direction.y

    def get_deus(self, random_bonus, x):
        block = Brick(x, 0, 1)

        if random_bonus == common.Bonuses.DecreaseBonus.value:
            bonus = ShrinkBonus(block.left, block.top)
        elif random_bonus == common.Bonuses.ExpandBonus.value:
            bonus = ExpandBonus(block.left, block.top)
        elif random_bonus == common.Bonuses.FireBallBonus.value:
            bonus = FireballBonus(block.left, block.top)
        elif random_bonus == common.Bonuses.FastBallBonus.value:
            bonus = FastBallBonus(block.left, block.top)
        elif random_bonus == common.Bonuses.LifeBonus.value:
            bonus = LifeBonus(block.left, block.top)
        else:
            bonus = DeathBonus(block.left, block.top)

        if random_bonus != -1:
            self.player1.bonuses.add(bonus)
            self.player2.bonuses.add(bonus)

    def get_bonus(self, block):
        chance = random.random()
        if chance > 0.7:
            random_bonus = BonusObject.get_random_bonus()

            if random_bonus == common.Bonuses.DecreaseBonus:
                bonus = ShrinkBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.ExpandBonus:
                bonus = ExpandBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.FireBallBonus:
                bonus = FireballBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.FastBallBonus:
                bonus = FastBallBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.LifeBonus:
                bonus = LifeBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.DeathBonus:
                bonus = DeathBonus(block.left, block.top)

            self.player1.bonuses.add(bonus)
            self.player2.bonuses.add(bonus)

    def remove_blocks(self, blocks_to_remove):
        block = next(iter(blocks_to_remove))

        if self.ball.state != common.BallState.Powerful:
            ball = self.ball
            delta = ball.center - block.center
            ball.direction.normalize()

            # odbijanje lopte o blok (promena znaka odgovarajuce koordinate)
            if abs(delta.x) - ball.velocity * abs(cos(ball.direction.x)) <= block.width / 2:
                ball.direction.y = -ball.direction.y
            else:
                ball.direction.x = -ball.direction.x

        self.level.blocks -= blocks_to_remove

        # dodela bonusa (moguca, zavisi od random vrednosti)
        self.get_bonus(block)

        # dodela bodova odgovarajucem igracu
        if self.paddle_reflect_ball == 1:
            self.player1.get_score(len(blocks_to_remove))
        elif self.paddle_reflect_ball == 2:
            self.player2.get_score(len(blocks_to_remove))

    def remove_bonuses(self):
        # aktivacija i brisanje bonusa za prvog igraca
        bonuses_to_remove = set()
        for bonus1 in self.player1.bonuses:
            if not bonus1.contact_two_frames(self):
                bonuses_to_remove.add(bonus1)
        for bonus2 in self.player2.bonuses:
            if not bonus2.contact_two_frames(self):
                bonuses_to_remove.add(bonus2)

        for bonus in self.player1.bonuses:
            bonus.move()
            if bonus.contact_two_frames(self.paddle1):
                bonus.activate(self, 1)
                bonuses_to_remove.add(bonus)

        # aktivacija i brisanje bonusa za drugog igraca
        for bonus in self.player2.bonuses:
            bonus.move()
            if bonus.contact_two_frames(self.paddle2):
                bonus.activate(self, 2)
                bonuses_to_remove.add(bonus)

        self.player1.bonuses -= bonuses_to_remove
        self.player2.bonuses -= bonuses_to_remove

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
        self.border_line = self.paddle.bottom - self.paddle.frame.height / 2  # granicka linija ispod koje loptica ne sme pasti

        self.levels = LevelCreator.get_levels(size)
        self.level = self.levels[self.current_level]

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
        for bonus in self.player.bonuses:
            yield bonus

    def reset(self):
        self.player.bonuses = set()
        self.paddle = Paddle(1, (self.size.width - common.PADDLE_SIZE.width) / 2,
                             self.size.height - common.PADDLE_SIZE.height)
        ball_x = self.paddle.x + (self.paddle.width - common.BALL_SIZE.width) / 2
        ball_y = self.paddle.top - common.BALL_SIZE.height
        self.ball = Ball(ball_x, ball_y)
        self.ball.reset_accelerate()
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

    def update_moving_objects(self, key):
        if key == Qt.Key_Right:
            old_x1 = self.paddle.left
            self.paddle.move(1)
            self.normalize_paddle_location()
            # pomeranje lopte
            if self.ball.state == BallState.Caught:
                self.ball.move(self.paddle.left - old_x1)
                self.reflect_ball()

        elif key == Qt.Key_Left:
            old_x1 = self.paddle.left
            self.paddle.move(-1)
            self.normalize_paddle_location()
            # pomeranje lopte
            if self.ball.state == BallState.Caught:
                self.ball.move(self.paddle.left - old_x1)
                self.reflect_ball()

    def tick(self, turn_rate=0):
        """ Promene polozaja objekata na svaki otkucaj tajmera"""

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

        # detekcija kolizije lopte i bloka
        blocks_to_remove = set()
        for block in self.level.blocks:
            if block.contact_two_frames(self.ball):
                blocks_to_remove.add(block)

        if len(blocks_to_remove) != 0:
            self.remove_blocks(blocks_to_remove)

        self.remove_bonuses()

        # detekcija kolizije lopte i paddle-a, racunanje smera odbijanja lopte
        if self.ball.contact_two_frames(self.paddle):
            mid = self.paddle.right - self.paddle.width / 2
            ball_mid = self.ball.right - self.ball.width / 2
            self.ball.direction = Vector.from_angle(-pi / 2 + (pi / 2.75 * (ball_mid - mid) / (self.paddle.width / 2)))

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
        if chance > 0.7:
            random_bonus = BonusObject.get_random_bonus()

            if random_bonus == common.Bonuses.DecreaseBonus:
                bonus = ShrinkBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.ExpandBonus:
                bonus = ExpandBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.FireBallBonus:
                bonus = FireballBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.FastBallBonus:
                bonus = FastBallBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.LifeBonus:
                bonus = LifeBonus(block.left, block.top)
            elif random_bonus == common.Bonuses.DeathBonus:
                bonus = DeathBonus(block.left, block.top)

            self.player.bonuses.add(bonus)

    def remove_blocks(self, blocks_to_remove):
        block = next(iter(blocks_to_remove))

        if self.ball.state != common.BallState.Powerful:
            ball = self.ball
            delta = ball.center - block.center
            ball.direction.normalize()

            # odbijanje lopte o blok (promena znaka odgovarajuce koordinate)
            if abs(delta.x) - ball.velocity * abs(cos(ball.direction.x)) <= block.width / 2:
                ball.direction.y = -ball.direction.y
            else:
                ball.direction.x = -ball.direction.x

        self.level.blocks -= blocks_to_remove

        # dodela bonusa (moguca, zavisi od random vrednosti)
        self.get_bonus(block)

        # dodela bodova
        self.player.get_score(len(blocks_to_remove))

    def remove_bonuses(self):
        bonuses_to_remove = {bonus for bonus in self.player.bonuses if not bonus.contact_two_frames(self)}

        for bonus in self.player.bonuses:
            bonus.move()
            if bonus.contact_two_frames(self.paddle):
                bonus.activate(self)
                bonuses_to_remove.add(bonus)

        self.player.bonuses -= bonuses_to_remove

    def kill_player(self):
        self.player.lose_life()
        self.reset()

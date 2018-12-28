from abstract_objects import BonusObject
import common


class ExpandBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        if paddle_flag == 1:
            game.paddle1.expand()
        elif paddle_flag == 2:
            game.paddle2.expand()
        else:
            game.paddle.expand()


class FireballBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        game.ball.change_state(common.BallState.Powerful)


class LifeBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        if paddle_flag == 1:
            game.player1.gain_life()
        elif paddle_flag == 2:
            game.player2.gain_life()
        else:
            game.player.gain_life()

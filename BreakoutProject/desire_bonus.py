from abstract_objects import BonusObject
import common


class ExpandBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.paddle.expand()


class FireballBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ball.change_state(common.BallState.Powerful)


class LifeBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.player.gain_life()

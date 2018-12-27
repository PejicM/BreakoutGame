from abstract_objects import BonusObject


class ShrinkBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.paddle.shrink()


class FastBallBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.ball.accelerate()


class DeathBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game):
        game.kill_player()

from abstract_objects import BonusObject


class ShrinkBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        if paddle_flag == 1:
            game.paddle1.shrink()
        elif paddle_flag == 2:
            game.paddle2.shrink()
        else:
            game.paddle.shrink()


class FastBallBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        game.ball.accelerate()


class DeathBonus(BonusObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activate(self, game, paddle_flag=0):
        if paddle_flag == 1:
            game.player1.lives -= 1
        elif paddle_flag == 2:
            game.player2.lives -= 1
        else:
            game.kill_player()

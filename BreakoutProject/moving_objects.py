from abstract_objects import MovingObject
import common
import os.path


class Paddle(MovingObject):
    def __init__(self, paddle_id=1, x=0, y=0):
        super().__init__(x, y, common.PADDLE_SIZE, common.PADDLE_VELOCITY, common.PADDLE_DIRECTION)
        self.paddle_id = paddle_id

    def get_image(self):
        return os.path.join('images', '%s.png' % (type(self).__name__.lower() + str(self.paddle_id)))

    def expand(self):
        self.frame = self.frame.transform(-self.frame.width / 2, 0, int(self.frame.width / 2, 0))

    def shrink(self):
        self.frame = self.frame.transform(self.frame.width / 2, 0, -int(self.frame.width / 2), 0)


class Ball(MovingObject):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, common.BALL_SIZE, common.BALL_VELOCITY,
                         common.BALL_DIRECTION)
        self.state = common.BallState.Free
        self.was_reflected = False

    def change_state(self, state):
        self.state = state

    def stick_to_paddle(self):
        self.change_state(common.BallState.Caught)

    def move(self, x=None):
        if self.state != common.BallState.Cought:
            super().move()
        else:
            self.frame = self.frame.relocate(x, 0)

    def accelerate(self):
        self.velocity = 1.5*common.BALL_VELOCITY

    def get_image(self):
        if self.state != common.BallState.Powerful:
            return  super().get_image()
        else:
            return os.path.join('images', 'fireball_bonus.png')

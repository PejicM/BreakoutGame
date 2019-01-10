import math
import random
import os.path
import common
from base import Frame, Vector


class Object:
    def __init__(self, x, y, size):
        self.frame = Frame(x, y, *size)

    @property
    def x(self):
        return self.frame.x

    @property
    def y(self):
        return self.frame.y

    @property
    def width(self):
        return self.frame.width

    @property
    def height(self):
        return self.frame.height

    @property
    def top(self):
        return self.frame.top

    @property
    def bottom(self):
        return self.frame.bottom

    @property
    def middle(self):
        return self.frame.middle

    @property
    def left(self):
        return self.frame.left

    @property
    def right(self):
        return self.frame.right

    @property
    def center(self):
        return self.frame.center

    @property
    def location(self):
        return self.frame.location

    @location.setter
    def location(self, location):
        self.frame.location = location

    def contact_two_frames(self, other):
        return self.frame.contact_two_frames(other.frame)

    def resize(self, d_width, d_height):
        self.frame = self.frame.resize(d_width, d_height)

    def relocate(self, delta_x, delta_y):
        self.frame = self.frame.relocate(delta_x, delta_y)

    def transform(self, delta_x, delta_y, d_width, d_height):
        return self.relocate(delta_x, delta_y).resize(d_width, d_height)

    def get_image(self):
        return os.path.join('images', '%s.png' % type(self).__name__.lower())


class MovingObject(Object):
    def __init__(self, x, y, size, velocity, direction):
        super().__init__(x, y, size)
        self.velocity = velocity
        self.direction = Vector(*direction)

    def move(self, turn_rate=1):
        direction_angle = self.direction.angle
        x = math.cos(direction_angle) * self.velocity * turn_rate
        y = math.sin(direction_angle) * self.velocity * turn_rate
        self.frame = self.frame.relocate(x, y)


class BonusObject(MovingObject):
    def __init__(self, x, y):
        super().__init__(x, y, common.BONUS_SIZE, common.BONUS_VELOCITY, common.BONUS_DIRECTION)

    def activate(self, game, paddle_flag=0):
        pass

    @staticmethod
    def get_random_bonus(index: int):
        return index

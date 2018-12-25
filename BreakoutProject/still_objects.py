import common
from abstract_objects import Object


class Brick(Object):
    def __init__(self, x, y, color=None):
        super().__init__(x, y, common.BRICK_SIZE)
        self.color = color

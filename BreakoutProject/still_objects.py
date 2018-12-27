import common
from abstract_objects import Object
import os.path


class Brick(Object):
    def __init__(self, x, y,brick_id, color=None):
        super().__init__(x, y, common.BRICK_SIZE)
        self.color = color
        self.brick_id = brick_id

    def get_image(self):
        return os.path.join('images', 'brick%s.png' % self.brick_id.__str__())

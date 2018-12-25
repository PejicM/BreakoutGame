import common
from still_objects import Brick


class Level:
    def __init__(self, level, blocks):
        self.level = level
        self.blocks = blocks


class LevelCreator:
    @staticmethod
    def get_levels(game_size):
        levels = {}
        colons = 10
        rows = 11

        level = 1
        width = (game_size.width - colons * common.BRICK_SIZE.width)/2
        height = 50

        blocks = {}
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 0 or j == 0 or j == 9:
                    blocks.add(LevelCreator._create_block(width, height, i, j))

        levels[level] = Level(level, blocks)

    @staticmethod
    def _create_block(width, height, i, j):
        block_location = LevelCreator._get_block_location(width, height, i, j)
        return Brick(*block_location)

    @staticmethod
    def _get_block_location(width, height, i, j):
        block_x = width + common.BRICK_SIZE.width * j
        block_y = height + common.BRICK_SIZE.height * i
        return block_x, block_y

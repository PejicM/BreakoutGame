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
        colons = 13
        rows = 8

        # LEVEL 1
        level = 1
        width = (game_size.width - colons * common.BRICK_SIZE.width)/2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                blocks.add(LevelCreator._create_block(width, height, i, j, 2))

        levels[level] = Level(level, blocks)

        # LEVEL 2
        level = 2
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 0 or j == 0 or j == 9:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 2))

        levels[level] = Level(level, blocks)

        return levels

    @staticmethod
    def _create_block(width, height, i, j, brick_id):
        block_location = LevelCreator._get_block_location(width, height, i, j)
        return Brick(*block_location,brick_id)

    @staticmethod
    def _get_block_location(width, height, i, j):
        block_x = width + common.BRICK_SIZE.width * j
        block_y = height + common.BRICK_SIZE.height * i
        return block_x, block_y

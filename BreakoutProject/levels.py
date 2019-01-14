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

        """ Level 1 """
        level = 1
        width = (game_size.width - colons * common.BRICK_SIZE.width)/2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 1:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 2))

        levels[level] = Level(level, blocks)

        """ Level 2 """
        level = 2
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 0 or j == 0 or j == 9:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 2))

        levels[level] = Level(level, blocks)

        """ Level 3 """
        level = 3
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 2))
                if j % 4 == 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 3))

        levels[level] = Level(level, blocks)

        """ Level 4 """
        level = 4
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if i % 2 == 0 and j % 2 == 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 2))
                if i % 2 == 1 and j % 2 == 1:
                    blocks.add(LevelCreator._create_block(width, height, i, j, 3))

        levels[level] = Level(level, blocks)

        """ Level 5 """
        level = 5
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        for i in range(rows):
            for j in range(colons):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    if i <= 3 and j != 6:
                        blocks.add(LevelCreator._create_block(width, height, i, j, 3))
                    elif i > 3 and j != 6:
                        blocks.add(LevelCreator._create_block(width, height, i, j, 2))
                    if j == 6:
                        blocks.add(LevelCreator._create_block(width, height, i, j, 1))

        levels[level] = Level(level, blocks)

        """ Level 6 """
        level = 6
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 0, 0, 0, 0, 3, 1, 2, 0, 0, 0, 0, 3],
                  [0, 2, 0, 0, 3, 0, 1, 0, 2, 0, 0, 3, 0],
                  [0, 0, 2, 3, 0, 0, 1, 0, 0, 2, 3, 0, 0],
                  [0, 0, 3, 2, 0, 0, 1, 0, 0, 3, 2, 0, 0],
                  [0, 3, 0, 0, 2, 0, 1, 0, 3, 0, 0, 2, 0],
                  [3, 0, 0, 0, 0, 2, 1, 3, 0, 0, 0, 0, 2],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]];
        for i in range(rows):
            for j in range(colons):
                if matrix[i][j] != 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, matrix[i][j]))

        levels[level] = Level(level, blocks)

        """ Level 7 """
        level = 7
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [0, 2, 0, 0, 3, 0, 1, 0, 2, 0, 0, 3, 0],
                  [2, 0, 2, 3, 0, 3, 1, 2, 0, 2, 3, 0, 3],
                  [0, 2, 0, 0, 3, 0, 1, 0, 2, 0, 0, 3, 0],
                  [0, 3, 0, 0, 2, 0, 1, 0, 3, 0, 0, 2, 0],
                  [3, 0, 3, 2, 0, 2, 1, 3, 0, 3, 2, 0, 2],
                  [0, 3, 0, 0, 2, 0, 1, 0, 3, 0, 0, 2, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]];
        for i in range(rows):
            for j in range(colons):
                if matrix[i][j] != 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, matrix[i][j]))

        levels[level] = Level(level, blocks)

        """ Level 8 """
        level = 8
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        matrix = [[2, 2, 2, 2, 0, 0, 1, 0, 0, 3, 3, 3, 3],
                  [2, 2, 2, 0, 0, 1, 1, 1, 0, 0, 3, 3, 3],
                  [2, 2, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3, 3],
                  [2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 3],
                  [3, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2],
                  [3, 3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 2, 2],
                  [3, 3, 3, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2],
                  [3, 3, 3, 3, 0, 0, 1, 0, 0, 2, 2, 2, 2]];
        for i in range(rows):
            for j in range(colons):
                if matrix[i][j] != 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, matrix[i][j]))

        levels[level] = Level(level, blocks)

        """ Level 9 """
        level = 9
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 1],
                  [1, 2, 2, 0, 0, 3, 3, 3, 0, 0, 2, 2, 1],
                  [1, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1],
                  [1, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1],
                  [1, 2, 2, 0, 0, 3, 3, 3, 0, 0, 2, 2, 1],
                  [1, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]];
        for i in range(rows):
            for j in range(colons):
                if matrix[i][j] != 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, matrix[i][j]))

        levels[level] = Level(level, blocks)

        """ Level 10 """
        level = 10
        width = (game_size.width - colons * common.BRICK_SIZE.width) / 2
        height = 80

        blocks = set()
        matrix = [[2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1],
                  [2, 2, 1, 1, 3, 3, 3, 1, 1, 2, 2, 2, 1],
                  [2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2],
                  [2, 2, 1, 1, 3, 3, 3, 1, 1, 2, 2, 2, 1],
                  [2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1],
                  [3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1],
                  [3, 3, 1, 1, 2, 2, 2, 1, 1, 3, 3, 3, 1],
                  [3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
                  [3, 3, 1, 1, 2, 2, 2, 1, 1, 3, 3, 3, 1],
                  [3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1]];
        for i in range(10):
            for j in range(colons):
                if matrix[i][j] != 0:
                    blocks.add(LevelCreator._create_block(width, height, i, j, matrix[i][j]))

        levels[level] = Level(level, blocks)

        return levels

    @staticmethod
    def _create_block(width, height, i, j, brick_id):
        block_location = LevelCreator._get_block_location(width, height, i, j)
        return Brick(*block_location, brick_id)

    @staticmethod
    def _get_block_location(width, height, i, j):
        block_x = width + common.BRICK_SIZE.width * j
        block_y = height + common.BRICK_SIZE.height * i
        return block_x, block_y

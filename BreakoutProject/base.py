import math


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return 'x:%s, y:%s' % (self.x, self.y)


class Frame:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def middle(self):
        return self.bottom - int(self.height / 2)

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def center(self):
        return Location(self.left + self.width / 2, self.top + self.height / 2)

    @property
    def location(self):
        return Location(self.x, self.y)

    @location.setter
    def location(self, location):
        self.x, self.y = location

    def contact_two_frames(self, frame):
        """Returns True if two frames are in contact"""
        return min(self.right, frame.right) >= max(self.left, frame.left) and min(self.bottom, frame.bottom) >= max(self.top, frame.top)

    def resize(self, width, height):
        """Returns resized frame"""
        return Frame(self.x, self.y, self.width + width, self.height + height)

    def relocate(self, x, y):
        """Return relocated frame"""
        return Frame(self.x + x, self.y + y, self.width,self.height)

    def transform(self, x, y, width, height):
        """Returns transformed frame"""
        return self.relocate(x, y).resize(width, height)

    def __str__(self):
        return '(%s, %s), width: %s, height: %s' % (self.x, self.y, self.width, self.height)


class Vector:
    """Usage: setting direction for moving objects"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def create(cls, vector):
        return cls(vector.x, vector.y)

    @classmethod
    def from_angle(cls, angle):
        return cls(math.cos(angle), math.sin(angle))

    def normalize(self):
        length = math.sqrt(self.x * self.x + self.y * self.y)
        self.x /= length
        self.y /= length

    @property
    def angle(self):
        return math.atan2(self.y, self.x)

# Task 5: Extending a Class

import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def euclidian_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Vector(Point):
    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)


p1 = Point(1, 5)
p2 = Point(10, 20)
print(p1)
print(p2)
print("Are points equal?", p1 == p2)
print("Distance between points:", p1.euclidian_distance(p2))

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1)
print(v2)
v3 = v1 + v2
print(v3)

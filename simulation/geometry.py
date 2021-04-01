import math
import random


class Point():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def update(self, speed, theta):
        self.__x = self.__x + speed * math.cos(theta)
        self.__y = self.__y + speed * math.sin(theta)

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def __str__(self):
        return f"({self.__x},{self.__y})"

    def __repr__(self):
        return f"({self.__x},{self.__y})"

    def distance(self, other):
        return abs(self.x() - other.x()) + abs(self.y() - other.y())

    def __add__(self, other):
        return Point(self.__x + other.x(), self.__y + other.y())


class Rectangle():
    def __init__(self, x, y, w, h):
        self.__top_left = Point(x, y)
        self.__width = w
        self.__height = h

    def contains(self, point: Point):
        return self.__top_left.x() <= point.x() <= self.__top_left.x() + \
            self.__width and self.__top_left.y() <= point.y() <= self.__top_left.y() + self.__height

    def rebound(self, pose: Point, current_theta: float):
        new_theta = current_theta
        # Exit through vertical walls
        if pose.x() <= self.__top_left.x() or pose.x() >= self.__top_left.x() + self.__width:
            new_theta = math.pi - current_theta
        # Exit through horizontal walls
        if pose.y() <= self.__top_left.y() or pose.y(
        ) >= self.__top_left.y() + self.__height:
            new_theta = 2 * math.pi - new_theta
        return new_theta

    def random_point(self, seed):
        x = random.uniform(
            self.__top_left.x(),
            self.__top_left.x() +
            self.__width)
        y = random.uniform(
            self.__top_left.y(),
            self.__top_left.y() +
            self.__height)
        return Point(x, y)

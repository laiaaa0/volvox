from simulation.geometry import Rectangle, Point
from simulation.agent import Agent

import unittest
import math


class TestPoint(unittest.TestCase):
    def test_init(self):
        rect = Rectangle(-10, -10, 20, 20)
        point = rect.random_point(42)
        a = Agent(rect, 0.3, math.pi / 2, point)
        self.assertEqual(point, a.position())

import unittest
import simulation.geometry as geo
import random
import math

class TestPoint(unittest.TestCase):

    def test_initialiser(self):
        random.seed(3)
        values = [(random.randint(-10,10), random.randint(-10,10)) for _ in range(10)]
        for (x,y) in values:
            point = geo.Point(x,y)
            self.assertEqual(x, point.x())
            self.assertEqual(y, point.y())

    def test_updater(self):
        random.seed(3)
        values = [(random.uniform(-10,10), random.uniform(-10,10), random.uniform(0,1), random.uniform(0,2*math.pi)) for _ in range(10)]
        
        for (x,y, speed,theta) in values:
            point = geo.Point(x,y)
            point.update(speed,theta)
            self.assertAlmostEqual(x + speed*math.cos(theta), point.x())
            self.assertAlmostEqual(y + speed*math.sin(theta), point.y())



if __name__ == "__main__":
    unittest.main()
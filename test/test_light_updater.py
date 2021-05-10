
import unittest
import numpy as np
import simulation.light_updater as light
from simulation.geometry import Point

class TestLightUpdater(unittest.TestCase):

    def test_add_square(self):
        # Middle square
        array = np.zeros((10,10))
        array[2:6,2:6] = 1
        other_array = np.zeros((10,10))
        light.add_square(other_array, Point(4,4),4)
        np.testing.assert_array_equal(array,other_array)

        # Bottom right square
        array = np.zeros((10,10))
        array[7:,7:] = 1
        other_array = np.zeros((10,10))
        light.add_square(other_array, Point(9,9),4)    
        np.testing.assert_array_equal(array,other_array)

        # Top square
        array = np.zeros((10,10))
        array[:3,:3] = 1
        other_array = np.zeros((10,10))
        light.add_square(other_array, Point(0,0),6)  
        np.testing.assert_array_equal(array,other_array)


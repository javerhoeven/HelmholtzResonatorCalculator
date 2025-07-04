import unittest
from calculation import Aperture


class TestAperture(unittest.TestCase):

    def setUp(self):
        print("Set Up")
        self.tube_1 = Aperture('tube', 0.1, 0.02)

    def test_area_calculation(self):
        self.assertAlmostEqual(self.tube_1.area, 0.001256637061)
    

if __name__ == '__main__':
    unittest.main()

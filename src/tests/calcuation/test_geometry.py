import unittest
from calculation import Geometry

class TestGeometry(unittest.TestCase):

    # TODO: add cylinders, further tests
    def setUp(self):
        self.cuboid_1 = Geometry('cuboid', x=0.1, y=0.1, z=0.1)
        self.cuboid_2 = Geometry('cuboid', x=0.1, y=0.5, z=0.3)

    def test_cuboid_args(self):
        with self.assertRaises(ValueError):
            Geometry('cuboid', x=0.2, y=0.3)

    def test_volume(self):
        self.assertEqual(self.cuboid_1.volume, 0.1**3)
        self.assertEqual(self.cuboid_2.volume, 0.1*0.5*0.3)



if __name__ == '__main__':
    unittest.main()
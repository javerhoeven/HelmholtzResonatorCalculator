
import unittest
from calculation import Geometry
from calculation import Aperture
from calculation import Resonator

class TestResonator(unittest.TestCase):
    """
    Unit tests for the Resonator class which works as a container for aperture and geometry.
    """

    def setUp(self):
        """
        Creates a sample Resonator instance using a cuboid geometry and tube aperture.
        
        """
        self.geometry = Geometry(form='cuboid', x=0.5, y=0.5, z=0.5)
        self.aperture = Aperture(form='tube', radius=0.01, length=0.05)
        self.resonator = Resonator(geometry=self.geometry, aperture=self.aperture)

    def test_initialization(self):
        """
        Tests if Resonator initializes correctly with given Geometry and Aperture instances.
        """
        self.assertIsInstance(self.resonator.geometry, Geometry)
        self.assertIsInstance(self.resonator.aperture, Aperture)

    def test_to_dict_structure_and_values(self):
        """
        Tests whether `to_dict()` returns a dictionary with the correct structure
        and expected values for form and radius of apperture.
        """
        result = self.resonator.to_dict()
        self.assertIn('geometry', result)
        self.assertIn('aperture', result)
        self.assertEqual(result['aperture']['form'], 'tube')
        self.assertAlmostEqual(result['aperture']['radius'], 0.01)

    def test_from_dict_reconstruction(self):
        """
        Tests whether a Resonator can be correctly restructured from its representation in the dictionary.
        """
        reconstructed = Resonator.from_dict(self.resonator.to_dict())
        self.assertAlmostEqual(reconstructed.aperture.radius, self.aperture.radius)
        self.assertAlmostEqual(reconstructed.geometry.volume, self.geometry.volume)

if __name__ == '__main__':
    unittest.main()

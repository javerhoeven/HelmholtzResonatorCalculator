import unittest
import numpy as np
from traits.api import TraitError
from src.calculation import SimulationParameters
from src.calculation import Medium


class TestSimulationParameters(unittest.TestCase):
    """
    Unit tests for the SimulationParameters class.
    These tests check the correctness of frequency calculation,
    physical relationships, and input validation via Traits.
    """

    def setUp(self):
        """Set up a default Medium and SimulationParameters instance for testing."""
        self.medium = Medium()
        self.sim = SimulationParameters(medium=self.medium)

    def test_freq_mon_increase(self):
        """
        Test that the generated frequency vector is strictly increasing.
        Ensures that no invalid or unordered values exist.
        """
        self.assertTrue(np.all(np.diff(self.sim.frequencies) > 0))

    def test_dependent_arrays(self):
        """
        Test that the arrays omega, k, and wavelength are computed correctly.
        Verifies physical relationships:
        omega = 2πf, k = omega / c, λ = c / f.
        """
        self.assertTrue(np.allclose(self.sim.omega, 2 * np.pi * self.sim.frequencies))
        self.assertTrue(np.allclose(self.sim.k, self.sim.omega / self.medium.c))
        self.assertTrue(np.allclose(self.sim.wavelength, self.medium.c / self.sim.frequencies))

    def test_zero_values_per_octave_raises(self):
        """
        Test that setting values_per_octave to zero raises a TraitError.
        Zero would lead to invalid frequency vector size.
        """
        with self.assertRaises(TraitError):
            self.sim.values_per_octave = 0

    def test_values_per_octave_float_raises(self):
        """
        Test that assigning a float to values_per_octave raises a TraitError.
        Only integer values are allowed by the Trait definition.
        """
        with self.assertRaises(TraitError):
            self.sim.values_per_octave = 100.5

    def test_freq_range_too_low_trait_error(self):
        """
        Test that defining a frequency range with a minimum below 1.0 Hz raises a TraitError.
        The lower bound for freq_range is set to 1.0 Hz in the class definition.
        """
        with self.assertRaises(TraitError):
            SimulationParameters(medium=self.medium, freq_range=(0.0, 500.0))

    def test_frequency_vector_length(self):
        """
        Test that the number of calculated frequencies matches:
        number of octaves × values_per_octave.
        Ensures correct log spacing and resolution.
        """
        f_min, f_max = self.sim.freq_range
        n_octaves = np.log2(f_max / f_min)
        expected_len = int(n_octaves * self.sim.values_per_octave)
        self.assertEqual(len(self.sim.frequencies), expected_len)

    def test_diffuse_sets_angle_zero(self):
        """
        Test that setting assume_diffuse to True resets the angle of incidence to 0°.
        This mimics a uniformly distributed sound field.
        """
        self.sim.angle_of_incidence = 45.0
        self.sim.assume_diffuse = True
        self.sim.update()
        self.assertEqual(self.sim.angle_of_incidence, 0.0)


if __name__ == '__main__':
    unittest.main()
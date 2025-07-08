import unittest
import numpy as np

from calculation import SimulationParameters 
from calculation import Medium          

class TestSimulationParameters(unittest.TestCase):

    def setUp(self):
        self.medium = Medium()    
        self.sim    = SimulationParameters(medium=self.medium)

    def test_freq_mon_increase(self):
        self.assertTrue(np.all(np.diff(params.frequence))>0,'freq vec not steady increasing')


    def test_dependent_arrays(self):
        # ω = 2π f
        self.assertTrue(
            np.allclose(self.sim.omega,2 * np.pi * self.sim.frequencies))

        # k = ω / c
        self.assertTrue(
            np.allclose(self.sim.k,
                        self.sim.omega / self.medium.c))

        # λ = c / f      (oder 2π c / ω – beides äquivalent)
        self.assertTrue(
            np.allclose(self.sim.wavelength,
                        self.medium.c / self.sim.frequencies))

    # ------------------------------------------------------------------
    # Frequenzvektor-Länge entspricht Oktaven * Werte_pro_Oktave
    # ------------------------------------------------------------------
    def test_frequency_vector_length(self):
        f_min, f_max = self.sim.freq_range
        n_octaves = np.log2(f_max / f_min)
        expected_len = int(n_octaves * self.sim.values_per_octave)

        self.assertEqual(len(self.sim.frequencies),n_octaves*self.sim.values_per_octaves)

    
    # Diffuser Einfall erzwingt Winkel = 0°
   
    def test_diffuse_sets_angle_zero(self):
        self.sim.angle_of_incidence = 45.0
        self.sim.assume_diffuse = True
        self.sim.update()                           # löst Neu­berechnung aus

        self.assertEqual(self.sim.angle_of_incidence, 0.0)


if __name__ == '__main__':
    unittest.main()
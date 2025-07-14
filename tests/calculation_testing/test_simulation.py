
import unittest
import numpy as np
from src.calculation import Simulation, Resonator, SimulationParameters, Medium, Geometry, Aperture
from traits.api import TraitError

class TestAbsorberSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(
            resonator=Resonator(
                geometry=Geometry(form='cuboid', x=0.1, y=0.1, z=0.1),
                aperture=Aperture(form='tube', radius=0.01, length=0.02)
            ),
            sim_params=SimulationParameters(medium=Medium())
        )

    def test_friction_impedance_length(self):
        self.sim.calc_z_friction()
        self.assertEqual(len(self.sim.z_friction), len(self.sim.sim_params.frequencies))

    def test_absorption_calc_no_crash(self):
        self.sim.calc_absorbtion_area()

    #def test_resonance_freq_is_float(self):
        #self.sim.calc_absorbtion_area()
       # f_res = self.sim.resonance_frequency()
       # self.assertIsInstance(f_res, float)
       # self.assertGreater(f_res, 0.0)

    def test_q_factor_positive(self):
        self.sim.calc_absorbtion_area()
        q = self.sim.calc_q_factor()
        self.assertIsInstance(q, float)
        self.assertGreater(q, 0.0)

    #def test_plot_absorption_executes(self):
        #self.sim.calc_absorbtion_area()
        #self.sim.calc_q_factor()
        #self.sim.plot_absorbtion_area()

    def test_absorbtion_area_in_to_dict(self):
        self.sim.calc_absorbtion_area()
        result = self.sim.to_dict()
        self.assertIn("absorbtion_area", result)

    def test_max_absorbtion_area_in_to_dict(self):
        self.sim.calc_max_absorbtion_area(plot=False)
        result = self.sim.to_dict()
        self.assertIn("max_absorbtion_area", result)

    def test_q_factor_in_to_dict(self):
        self.sim.calc_absorbtion_area()
        self.sim.calc_q_factor()
        result = self.sim.to_dict()
        self.assertIn("q_factor", result)

    def test_z_friction_real_imag_in_to_dict(self):
        self.sim.calc_z_friction()
        result = self.sim.to_dict()
        self.assertIn("z_friction", result)


if __name__ == '__main__':
    unittest.main()




def test_absorbtion_area_in_to_dict(self):
    self.sim.calc_absorbtion_area()
    result = self.sim.to_dict()
    self.assertIn("absorbtion_area", result)

def test_max_absorbtion_area_in_to_dict(self):
    self.sim.calc_max_absorbtion_area(plot=False)
    result = self.sim.to_dict()
    self.assertIn("max_absorbtion_area", result)

def test_q_factor_in_to_dict(self):
    self.sim.calc_absorbtion_area()
    self.sim.calc_q_factor()
    result = self.sim.to_dict()
    self.assertIn("q_factor", result)

def test_z_friction_real_imag_in_to_dict(self):
    self.sim.calc_z_friction()
    result = self.sim.to_dict()
    self.assertIn("z_friction_real", result)
    self.assertIn("z_friction_imag", result)

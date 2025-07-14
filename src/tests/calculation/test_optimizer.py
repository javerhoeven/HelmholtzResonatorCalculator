import unittest

from src.calculation import Optimizer
from scipy.optimize import minimize
import click
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


class TestOptimizer(unittest.TestCase):

    def setUp(self):
        """Initialisiert einen Optimizer mit realistischen Zielwerten."""
        self.f_target = 300.0
        self.q_target = 5.0
        self.optimizer = Optimizer(f_target=self.f_target, q_target=self.q_target)

    def test_initialization(self):
        """Testet, ob die Initialisierung korrekt ist."""
        self.assertEqual(self.optimizer.f_target, self.f_target)
        self.assertEqual(self.optimizer.q_target, self.q_target)

    def test_generate_initial_set_valid(self):
        """Testet, ob gültige Startwerte generiert werden können."""
        self.optimizer.bounds = [
            (0.1, 1.0),  # x
            (0.1, 1.0),  # y
            (0.1, 1.0),  # z
            (0.01, 0.1),  # radius
            (0.01, 0.3),  # length
            (1, 5000),    # xi
        ]
        values = self.optimizer.generate_initial_set()
        self.assertIsNotNone(values)
        self.assertEqual(len(values), 6)
        for val, (low, high) in zip(values, self.optimizer.bounds):
            self.assertGreaterEqual(val, low)
            self.assertLessEqual(val, high)

    def test_objective_output_validity(self):
        """Testet, ob die objective-Funktion einen float-Wert zurückgibt."""
        self.optimizer.bounds = [
            (0.5, 0.6),  # x
            (0.5, 0.6),  # y
            (0.5, 0.6),  # z
            (0.05, 0.06),  # radius
            (0.05, 0.06),  # length
            (100, 200)     # xi
        ]
        x0 = [0.55, 0.55, 0.55, 0.055, 0.055, 150]
        result = self.optimizer.objective(x0)
        self.assertIsInstance(result, float)

    def test_run_single_optimization_returns_result(self):
        """Testet, ob die Optimierung mit fixen Startwerten funktioniert."""
        self.optimizer.bounds = [
            (0.5, 0.6), (0.5, 0.6), (0.5, 0.6),
            (0.05, 0.06), (0.05, 0.06), (100, 200)
        ]
        x0 = [0.55, 0.55, 0.55, 0.055, 0.055, 150]
        res = self.optimizer.run_single_optimization(x0)
        self.assertIsNotNone(res)
        self.assertTrue(hasattr(res, 'x'))
        self.assertTrue(hasattr(res, 'fun'))

if __name__ == '__main__':
    unittest.main()
import unittest
import numpy as np
from traits.api import TraitError

from calculation.medium import Medium


class TestMedium(unittest.TestCase):
    """
    Unit Tests für die Medium-Klasse.
    Testet Randwerte und Out-of-Range-Werte für Temperatur und relative Feuchte.
    """

    @classmethod
    def setUpClass(cls):
        """
        Liest einmalig die physikalischen Grenzen und Standardwerte aus den Traits der Medium-Klasse aus.
        """
        traits = Medium.class_traits()
        cls.temp_min = traits['temperature_celsius'].handler._low
        cls.temp_max = traits['temperature_celsius'].handler._high
        cls.temp_default = traits['temperature_celsius'].handler.default_value

        cls.humidity_min = traits['rel_humidity'].handler._low
        cls.humidity_max = traits['rel_humidity'].handler._high
        cls.humidity_default = traits['rel_humidity'].handler.default_value

    def expected_temperature_kelvin(self, temp_celsius):
        """Compute expected temperature in Kelvin."""
        return temp_celsius + 273.15

    def expected_speed_of_sound(self, temp_celsius, rel_humidity):
        """Compute expected speed of sound (m/s)."""
        return 331.3 + 0.606 * temp_celsius + 0.0124 * rel_humidity

    def expected_kinematic_viscosity(self, temp_celsius, rho):
        """Compute expected kinematic viscosity (m²/s)."""
        T = temp_celsius + 273.15
        mu0 = 1.716e-5
        T0 = 273.15
        C = 111
        mu = mu0 * ((T / T0) ** 1.5) * ((T0 + C) / (T + C))
        return mu / rho

    def expected_density(self, temp_celsius, rel_humidity):
        """Compute expected air density (kg/m³)."""
        T = temp_celsius + 273.15
        p = 1013.15 * 100
        phi = rel_humidity
        R_d = 287.05
        R_v = 461.5
        p_sat = 6.112 * np.exp(17.62 * T / (243.12 * T)) * 100
        p_v = phi * p_sat
        return (p - p_v) / (R_d * T) + p_v / (R_v * T)

    # ------------------------------------
    # Temperature edge tests (RH = default)
    # ------------------------------------
    def test_min_temperature_valid(self):
        """Check min temperature with default RH."""
        m = Medium(
            temperature_celsius=self.temp_min,
            rel_humidity=self.humidity_default
        )

        expected_rho = self.expected_density(self.temp_min, self.humidity_default)
        self.assertAlmostEqual(m.density, expected_rho, places=5)

        expected_visc = self.expected_kinematic_viscosity(self.temp_min, expected_rho)
        self.assertAlmostEqual(m.kinematic_viscosity, expected_visc, places=8)

        expected_kelvin = self.expected_temperature_kelvin(self.temp_min)
        self.assertAlmostEqual(m.temperature_kelvin, expected_kelvin, places=3)

        expected_c = self.expected_speed_of_sound(self.temp_min, self.humidity_default)
        self.assertAlmostEqual(m.c, expected_c, places=3)

    def test_max_temperature_valid(self):
        """Check max temperature with default RH."""
        m = Medium(
            temperature_celsius=self.temp_max,
            rel_humidity=self.humidity_default
        )

        expected_rho = self.expected_density(self.temp_max, self.humidity_default)
        self.assertAlmostEqual(m.density, expected_rho, places=5)

        expected_visc = self.expected_kinematic_viscosity(self.temp_max, expected_rho)
        self.assertAlmostEqual(m.kinematic_viscosity, expected_visc, places=8)

        expected_kelvin = self.expected_temperature_kelvin(self.temp_max)
        self.assertAlmostEqual(m.temperature_kelvin, expected_kelvin, places=3)

        expected_c = self.expected_speed_of_sound(self.temp_max, self.humidity_default)
        self.assertAlmostEqual(m.c, expected_c, places=3)

    # ------------------------------------
    # Humidity edge tests (Temp = default)
    # ------------------------------------
    def test_min_humidity_valid(self):
        """Check min RH with default temperature."""
        m = Medium(
            temperature_celsius=self.temp_default,
            rel_humidity=self.humidity_min
        )

        expected_rho = self.expected_density(self.temp_default, self.humidity_min)
        self.assertAlmostEqual(m.density, expected_rho, places=5)

        expected_visc = self.expected_kinematic_viscosity(self.temp_default, expected_rho)
        self.assertAlmostEqual(m.kinematic_viscosity, expected_visc, places=8)

        expected_kelvin = self.expected_temperature_kelvin(self.temp_default)
        self.assertAlmostEqual(m.temperature_kelvin, expected_kelvin, places=3)

        expected_c = self.expected_speed_of_sound(self.temp_default, self.humidity_min)
        self.assertAlmostEqual(m.c, expected_c, places=3)

    def test_max_humidity_valid(self):
        """Check max RH with default temperature."""
        m = Medium(
            temperature_celsius=self.temp_default,
            rel_humidity=self.humidity_max
        )

        expected_rho = self.expected_density(self.temp_default, self.humidity_max)
        self.assertAlmostEqual(m.density, expected_rho, places=5)

        expected_visc = self.expected_kinematic_viscosity(self.temp_default, expected_rho)
        self.assertAlmostEqual(m.kinematic_viscosity, expected_visc, places=8)

        expected_kelvin = self.expected_temperature_kelvin(self.temp_default)
        self.assertAlmostEqual(m.temperature_kelvin, expected_kelvin, places=3)

        expected_c = self.expected_speed_of_sound(self.temp_default, self.humidity_max)
        self.assertAlmostEqual(m.c, expected_c, places=3)

    # ------------------------------------
    # Out-of-range tests: Temperature
    # ------------------------------------
    def test_temp_minimally_too_small(self):
        """Should raise TraitError if temperature is minimally below min."""
        with self.assertRaises(TraitError):
            Medium(
                temperature_celsius=self.temp_min - 0.001,
                rel_humidity=self.humidity_default
            )

    def test_temp_minimally_too_large(self):
        """Should raise TraitError if temperature is minimally above max."""
        with self.assertRaises(TraitError):
            Medium(
                temperature_celsius=self.temp_max + 0.001,
                rel_humidity=self.humidity_default
            )

    # ------------------------------------
    # Out-of-range tests: Humidity
    # ------------------------------------
    def test_humidity_minimally_too_small(self):
        """Should raise TraitError if RH is minimally below min."""
        with self.assertRaises(TraitError):
            Medium(
                temperature_celsius=self.temp_default,
                rel_humidity=self.humidity_min - 0.001
            )

    def test_humidity_minimally_too_large(self):
        """Should raise TraitError if RH is minimally above max."""
        with self.assertRaises(TraitError):
            Medium(
                temperature_celsius=self.temp_default,
                rel_humidity=self.humidity_max + 0.001
            )



if __name__ == "__main__":
    unittest.main()
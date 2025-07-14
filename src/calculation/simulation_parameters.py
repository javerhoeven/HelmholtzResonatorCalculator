from traits.api import HasTraits, Instance, Tuple, Int, Float, Bool, Array
from traitsui.api import View, Item, Group
import numpy as np
from .medium import Medium  

class SimulationParameters(HasTraits):
    """
    Contains all frequency- and medium-related parameters required for Helmholtz simulations.

    This class manages the frequency range, discretization (values per octave), and 
    calculates all dependent physical quantities (angular frequency, wave number, wavelength).
    
    Attributes:
        medium (Medium): The propagation medium.
        freq_range (Tuple): Frequency range for the simulation (min, max).
        values_per_octave (int): Discretization of the frequency axis.
        angle_of_incidence (float): Angle of sound incidence (°). Ignored if `assume_diffuse` is True.
        assume_diffuse (bool): If True, sets angle_of_incidence to 0 and assumes diffuse field.
        frequencies (np.ndarray): Frequency vector.
        omega (np.ndarray): Angular frequency (rad/s).
        k (np.ndarray): Wave number (1/m).
        wavelength (np.ndarray): Wavelength (m).
    """

    medium = Instance(Medium)
    freq_range = Tuple(Float(0.01), Float(500.0))
    values_per_octave = Int(100)
    angle_of_incidence = Float(0.0)
    assume_diffuse = Bool(True)

    frequencies = Array(dtype=float)
    omega = Array(dtype=float)
    k = Array(dtype=float)
    wavelength = Array(dtype=float)

    def __init__(self, **traits):
        """
        Initialize and compute frequency-dependent parameters based on provided traits.

        Args:
            **traits: Keyword arguments for setting initial traits (e.g., medium, freq_range).
        """
        super().__init__(**traits)
        self.update()

    def update(self):
        """
        Recalculate all dependent parameters from the current configuration.
        Called automatically after initialization and whenever parameters change.
        """
        if self.assume_diffuse:
            self.angle_of_incidence = 0.0

        self.calculate_frequencies()
        self.omega = self.calc_omega(self.frequencies)
        self.k = self.calc_k(self.omega, self.medium.c)
        self.wavelength = self.calc_lambda(self.omega, self.medium.c)

    def calculate_frequencies(self):
        """
        Compute the logarithmic frequency vector based on the frequency range and values per octave.
        """
        f_min, f_max = self.freq_range
        n_octaves = np.log2(f_max / f_min)
        n_freq_values = int(n_octaves * self.values_per_octave)
        self.frequencies = np.logspace(np.log10(f_min), np.log10(f_max), num=n_freq_values)

    def calc_omega(self, frequencies):
        """
        Calculate angular frequency vector ω = 2πf.

        Args:
            frequencies (np.ndarray): Frequency vector.

        Returns:
            np.ndarray: Angular frequency vector (rad/s).
        """
        return 2 * np.pi * frequencies
    
    def calc_k(self, omega, c):
        """
        Calculate wave number vector k = ω / c.

        Args:
            omega (np.ndarray): Angular frequency.
            c (float): Speed of sound in the medium.

        Returns:
            np.ndarray: Wave number (1/m).
        """
        return omega / c
    
    def calc_lambda(self, omega, c):
        """
        Calculate wavelength λ = c / f = 2πc / ω.

        Args:
            omega (np.ndarray): Angular frequency.
            c (float): Speed of sound in the medium.

        Returns:
            np.ndarray: Wavelength (m).
        """
        return c / (omega / (2 * np.pi))
    
    def to_dict(self):
        """
        Convert all relevant parameters to a dictionary for serialization.

        Returns:
            dict: Dictionary representation of the simulation parameters.
        """
        return {
            "medium": self.medium.to_dict(),
            "freq_range": self.freq_range,
            "values_per_octave": self.values_per_octave,
            "angle_of_incidence": self.angle_of_incidence,
            "assume_diffuse": self.assume_diffuse
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Reconstructs a SimulationParameters instance from a dictionary.

        Args:
            data (dict): Dictionary with serialized values.

        Returns:
            SimulationParameters: A con
"""
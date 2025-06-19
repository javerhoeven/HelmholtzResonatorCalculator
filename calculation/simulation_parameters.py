import numpy as np
from .medium import Medium

class SimulationParameters():
    def __init__(self,
                 medium : Medium,
                 freq_range : tuple = (20, 500), # (low, high)
                 values_per_octave : int = 100, # frequency resolution
                 angle_of_incidence : float = None):
        
        # if angle is given, set to that angle
        # else: assume diffus incidence
        if angle_of_incidence is None:
            self.assume_diffuse = True
            self.angle_of_incidence = 0
        else:
            self.assume_diffuse = False
            self.angle_of_incidence = angle_of_incidence

        self.medium = medium

        # calculate frequency vector with log spacing
        self.f_min = freq_range[0]
        self.f_max = freq_range[1]
        n_octaves = np.log2(self.f_max / self.f_min)
        n_freq_values = int(n_octaves * values_per_octave)
        self.frequencies = np.logspace(np.log10(self.f_min), np.log10(self.f_max), num=n_freq_values)
        
        
        
        self.omega = self.calc_omega(self.frequencies)

        # calculate wave number and wavelength
        self.k = self.calc_k(self.omega, self.medium.c)
        self._lambda = self.calc_lambda(self.omega, self.medium.c)

    def calc_omega(self, frequencies):
            """Calculate angular frequency from frequency vector."""
            return 2 * np.pi * frequencies
    
    def calc_k(self, omega, c):
        """Calculate wave number from angular frequency and speed of sound."""
        return omega / c
    
    def calc_lambda(self, omega, c):
        """Calculate wavelength from angular frequency and speed of sound."""
        return c / (omega / (2 * np.pi))
    
    def to_dict(self):
        """Convert the simulation parameters to a dictionary representation."""
        return {
            "medium": self.medium.to_dict(),
            "frequencies": self.frequencies.tolist(),
            # "omega": self.omega.tolist(),
            # "k": self.k.tolist(),
            # "_lambda": self._lambda.tolist(),
            "angle_of_incidence": self.angle_of_incidence,
            "assume_diffuse": self.assume_diffuse
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creates a SimulationParameters instance from a dictionary"""
        medium = Medium.from_dict(data['medium'])
        frequencies = np.array(data['frequencies'])
        
        angle_of_incidence = data.get('angle_of_incidence', None)
        assume_diffuse = data.get('assume_diffuse', True)

        params = cls(medium=medium, angle_of_incidence=angle_of_incidence)
        params.frequencies = frequencies
        # recalculate omega, k, and lambda based on the frequencies
        params.omega = params.calc_omega(frequencies)
        params.k = params.calc_k(params.omega, medium.c)
        params._lambda = params.calc_lambda(params.omega, medium.c)
     
        params.assume_diffuse = assume_diffuse
        
        return params
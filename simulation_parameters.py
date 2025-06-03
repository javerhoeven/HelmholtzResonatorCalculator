import numpy as np
from medium import Medium

class SimulationParameters():
    def __init__(self,
                 medium : Medium,
                 freq_range : tuple = (20, 20e3), # (low, high)
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
        self.omega = 2 * np.pi * self.frequencies

        # calculate wave number and wavelength
        self.k = self.omega / self.medium.c
        self._lambda = self.medium.c / self.frequencies
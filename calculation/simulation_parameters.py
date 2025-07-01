from traits.api import HasTraits, Instance, Tuple, Int, Float, Bool, Property, Array, cached_property
from traitsui.api import View, Item, Group
import numpy as np
from medium import Medium  # Passe den Import ggf. an deinen Projekt-Ordner an!

class SimulationParameters(HasTraits):
    medium = Instance(Medium)
    freq_range = Tuple(Float(20.0), Float(500.0))
    values_per_octave = Int(100)
    angle_of_incidence = Float(0.0)
    assume_diffuse = Bool(True)

    frequencies = Array(dtype=float)
    omega = Array(dtype=float)
    k = Array(dtype=float)
    wavelength = Array(dtype=float)

    def __init__(self, **traits):
        super().__init__(**traits)
        self.update()

    def update(self):
        """Recalculate frequency vector and dependent parameters"""
        if self.assume_diffuse:
            self.angle_of_incidence = 0.0

        self.calculate_frequencies()
        self.omega = self.calc_omega(self.frequencies)
        self.k = self.calc_k(self.omega, self.medium.c)
        self.wavelength = self.calc_lambda(self.omega, self.medium.c)

    def calculate_frequencies(self):
        f_min, f_max = self.freq_range
        n_octaves = np.log2(f_max / f_min)
        n_freq_values = int(n_octaves * self.values_per_octave)
        self.frequencies = np.logspace(np.log10(f_min), np.log10(f_max), num=n_freq_values)

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
        
        # TraitsUI View
    traits_view = View(
        Group(
            Item('freq_range', label="Frequenzbereich (Hz)"),
            Item('values_per_octave', label="Werte pro Oktave"),
            Item('assume_diffuse', label="Diffuser Einfall?"),
            Item('angle_of_incidence', label="Einfallswinkel (°)", enabled_when='not assume_diffuse'),
        ),
        title="Simulation Parameters",
        buttons=['OK', 'Cancel'],
        resizable=True
    )

# Beispiel GUI starten
if __name__ == "__main__":
    # Beispiel-Medium
    air = Medium()
    sim_params = SimulationParameters(medium=air)
    sim_params.configure_traits()
    sim_params.update()
from traits.api import HasTraits, Float, Range, TraitError, Union
from traitsui.api import View, Item, Group
import numpy as np

class Medium(HasTraits):
    """
    Represents the physical properties of the medium (typically air) used in simulations.

    Automatically calculates density, speed of sound, and kinematic viscosity
    based on temperature and humidity if not explicitly provided.

    Attributes:
        temperature_celsius (float): Ambient temperature in °C (-50 to 60).
        rel_humidity (float): Relative humidity as a value between 0 and 1.
        density (float): Air density in kg/m³ (calculated or provided).
        speed_of_sound (float): Speed of sound in m/s (calculated or provided).
        c (float): Alias for speed_of_sound.
        temperature_kelvin (float): Temperature in Kelvin.
        kinematic_viscosity (float): Kinematic viscosity of air in m²/s.
    """

    # --- Input Parameter mit Traits Validierung ---
    temperature_celsius = Range(-50.0, 60.0, 20.0)
    rel_humidity = Range(0.0, 1.0, 0.5)

    density = Union(None, Float(min=0.0), value=None)  # kg/m³
    speed_of_sound = Union(None, Float(min=0.0))       # m/s

    # --- Automatisch berechnete Eigenschaften ---
    temperature_kelvin = Float
    kinematic_viscosity = Float
    c = Float  # Alias für speed_of_sound

    def __init__(self, **kwargs):
        """
        Initialize a Medium object with temperature and humidity.

        If `density` or `speed_of_sound` is not provided, they are calculated automatically.

        Raises:
            TraitError: If provided density or speed of sound is non-positive.
        """
        super().__init__(**kwargs)
        self.temperature_kelvin = self.temperature_celsius + 273.15

        if self.density is None:
            self.calc_density()
        elif self.density <= 0:
            raise TraitError("Density must be positive.")

        if self.speed_of_sound is None:
            self.calc_speed_of_sound()
        elif self.speed_of_sound <= 0:
            raise TraitError("speed of sound must be positive.")
        else:
            self.c = self.speed_of_sound

        self.calc_kinematic_viscosity()

    def calc_density(self):
        """
        Calculates air density using the Magnus equation.

        The density is calculated as:

        .. math::

            \\rho = \\frac{p - p_v}{R_d \\, T} + \\frac{p_v}{R_v \\, T}

        where:

        - :math:`p` atmospheric pressure (Pa)  
        - :math:`p_v = \\phi \\; p_{\\mathrm{sat}}` partial vapor pressure (Pa)  
        - :math:`p_{\\mathrm{sat}} = 6.112 \\, \\exp\\biggl(\\frac{17.62 \\, T}{243.12 + T}\\biggr) \\times 100` (Pa)  
        - :math:`\\phi` relative humidity (0…1)  
        - :math:`T` absolute temperature in Kelvin  
        - :math:`R_d = 287.05 \\; \\mathrm{J/(kg \\cdot K)}` gas constant for dry air  
        - :math:`R_v = 461.5 \\; \\mathrm{J/(kg \\cdot K)}` gas constant for water vapor  

        Raises:
        TraitError: If the result is non-positive.
         """
        p = 1013.15 * 100  # Atmospheric pressure in Pa
        T = self.temperature_kelvin
        phi = self.rel_humidity
        R_d = 287.05       # Gas constant for dry air
        R_v = 461.5        # Gas constant for water vapor

        p_sat = 6.112 * np.exp(17.62 * T / (243.12 * T)) * 100
        p_v = phi * p_sat

        rho = (p - p_v) / (R_d * T) + p_v / (R_v * T)

        if rho <= 0:
            raise TraitError("Calculated density must be > 0.")
        
        self.density = rho

    def calc_speed_of_sound(self):
        """
        Approximates the speed of sound based on DIN ISO 9613-1:1993.

        The formula used is:

        .. math::

            c = 331.3 + 0.606 \\,T + 0.0124 \\,\phi

        where:

        - :math:`T` ambient temperature in °C  
        - :math:`\phi` relative humidity (0…1)  
        - :math:`c` speed of sound in m/s
        """
        self.c = 331.3 + 0.606 * self.temperature_celsius + 0.0124 * self.rel_humidity

 
   

    def calc_kinematic_viscosity(self):
        r"""
        Calculates the kinematic viscosity of air using Sutherland's formula.

        The dynamic viscosity :math:`\mu` is calculated using:

        .. math::

            \mu = \mu_0 \left( \frac{T}{T_0} \right)^{3/2} \cdot \frac{T_0 + C}{T + C}

        where:

        - :math:`\mu_0 = 1.716 \times 10^{-5}\ \text{Pa·s}` (reference viscosity)
        - :math:`T_0 = 273.15\ \text{K}` (reference temperature)
        - :math:`C = 111\ \text{K}` (Sutherland's constant)
        - :math:`T` temperature in Kelvin

        The kinematic viscosity :math:`\nu` is then:

        .. math::

            \nu = \frac{\mu}{\rho}

        where :math:`\rho` is the air density in kg/m³.
        """


        T = self.temperature_kelvin
        mu0 = 1.716e-5  # Reference dynamic viscosity (Pa·s)
        T0 = 273.15     # Reference temperature (K)
        C = 111         # Sutherland's constant for air

        mu = mu0 * ((T / T0) ** 1.5) * ((T0 + C) / (T + C))
        self.kinematic_viscosity = mu / self.density

    def to_dict(self):
        """
        Converts the medium's properties to a dictionary.

        Returns:
            dict: Dictionary containing all relevant physical parameters.
        """
        return {
            "temperature_celsius": self.temperature_celsius,
            "temperature_kelvin": self.temperature_kelvin,
            "rel_humidity": self.rel_humidity,
            "density": self.density,
            "speed_of_sound": self.c,
            "kinematic_viscosity": self.kinematic_viscosity
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Medium instance from a dictionary.

        Args:
            data (dict): Dictionary with keys matching Medium attributes.

        Returns:
            Medium: A new Medium instance.
        """
        return cls(
            temperature_celsius=data['temperature_celsius'],
            rel_humidity=data['rel_humidity'],
            density=data.get('density'),
            speed_of_sound=data.get('speed_of_sound'))

    # TraitsUI View
    traits_view = View(
        Group(
            Item('temperature_celsius', label="Temperatur (°C)"),
            Item('rel_humidity', label="Relative Luftfeuchtigkeit"),
            Item('density', label="Dichte (kg/m³)", style='readonly'),
            Item('speed_of_sound', label="Schallgeschwindigkeit (m/s)", style='readonly'),
            Item('kinematic_viscosity', label="Kinematische Viskosität (m²/s)", style='readonly'),
        ),
        title="Medium Eigenschaften",
        buttons=['OK', 'Cancel'],
        resizable=True
    )


if __name__ == "__main__":
    medium = Medium()
    medium.configure_traits()

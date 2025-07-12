from traits.api import HasTraits, Float, Range, TraitError, Union
from traitsui.api import View, Item, Group
import numpy as np

class Medium(HasTraits):
    # --- Input Parameter mit Traits Validierung ---
    temperature_celsius = Range(-50.0, 60.0, 20.0)  # Raumtemperaturbereich
    rel_humidity = Range(0.0, 1.0, 0.5)  # Prozent als Dezimalwert (0 bis 1)

    density = Union(None, Float(min=0.0), value=None)  # kg/m³
    speed_of_sound = Union(None, Float(min=0.0)) # m/s

    # --- Automatisch berechnete Eigenschaften ---
    temperature_kelvin = Float
    kinematic_viscosity = Float

    c = Float  # Für interne Konsistenz (speed of sound, berechnet oder übergeben)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temperature_kelvin = self.temperature_celsius + 273.15

        if self.density is None:
            self.calc_density()
        else:
            if self.density <= 0:
                raise TraitError("Density must be positive.")

        if self.speed_of_sound is None:
            self.calc_speed_of_sound()
        else:
            if self.speed_of_sound <= 0:
                raise TraitError("speed of sound must be positive.")
            self.c = self.speed_of_sound

        self.calc_kinematic_viscosity()
        


    def calc_density(self):
        """calculate density based on Magnus equation. 
        Depends on relative humidity and temperature
        """
        # constants
        p = 1013.15 * 100 # atmospheric pressure in Pa
       
        T = self.temperature_kelvin
        phi = self.rel_humidity

        R_d = 287.05 # specific gas constant for dry air
        R_v = 461.5 # specific gas constant for water vapor

        p_sat = 6.112 * np.exp(17.62 * T / (243.12 * T)) * 100
        p_v = phi * p_sat

        rho = (p - p_v) / (R_d * T) + p_v / (R_v * T)
        if rho <= 0:
            raise TraitError("Calculated density must be > 0.")
        
        self.density = rho

    def calc_speed_of_sound(self):
        """This is an approximation according to DIN ISO 9613-1:1993"""
        self.c = 331.3 + 0.606 * self.temperature_celsius + 0.0124 * self.rel_humidity

    def calc_kinematic_viscosity(self): 
        """
        calculation based on sutherland's formula
        """
        T = self.temperature_kelvin
        mu0 = 1.716e-5
        T0 = 273.15
        C = 111     # Sutherland constant for air
        mu = mu0 * ((T/T0) ** 1.5) * ((T0 + C) / (T + C))
        self.kinematic_viscosity = mu / self.density

    def to_dict(self):
        """Convert the medium properties to a dictionary representation."""
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
        """Creates a Medium instance from a dictionary"""
        return cls(
            temperature=data['temperature_celsius'],
            rel_humidity=data['rel_humidity'],
            density=data.get('density'),
            speed_of_sound=data.get('speed_of_sound')
        )
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
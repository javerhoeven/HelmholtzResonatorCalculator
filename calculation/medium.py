import numpy as np

class Medium():

    def __init__(self,
                 temperature : float = 20., # in C
                 rel_humidity : float = 0.5,
                 density : float = None,
                 speed_of_sound : float = None):
        
        # TODO: check if rel_humidity is in range, temperature makes sense
        self.temperature_celsius = temperature
        self.temperature_kelvin = self.temperature_celsius + 273.15
        self.rel_humidity = rel_humidity

        # check if optional input parameters are given
        if density is None:
            self.calc_density()
        else:
            self.density = density

        if speed_of_sound is None:
            self.calc_speed_of_sound()
        else:
            self.c = speed_of_sound

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

        self.density = rho

    def calc_speed_of_sound(self):
        """This is an approximation according to 9613-1:1993"""
        self.c = 331.3 + 0.606 * self.temperature_celsius + 0.0124 * self.rel_humidity

    def calc_kinematic_viscosity(self): 
        """
        calculation based on sutherland's formula [GPT]
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
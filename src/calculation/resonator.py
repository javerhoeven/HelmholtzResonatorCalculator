from .geometry import Geometry
from .aperture import Aperture

class Resonator():
    def __init__(self, 
                 geometry : Geometry,
                 aperture : Aperture):
        self.geometry = geometry
        self.aperture = aperture

    def to_dict(self):
        """Convert the resonator to a dictionary representation."""
        return {
            "geometry": self.geometry.to_dict(),
            "aperture": {
                "form": self.aperture.form,
                "length": self.aperture.length,
                "radius": self.aperture.radius,
                "inner_ending": self.aperture.inner_ending,
                "outer_ending": self.aperture.outer_ending,
                "additional_dampening": self.aperture.additional_dampening,
                "xi": self.aperture.xi,
                "amount": self.aperture.amount,
                "width": self.aperture.width,
                "height": self.aperture.height
            }
        }
    @classmethod
    def from_dict(cls, data):
        """Creates a Resonator instance from a dictionary"""
        geometry = Geometry.from_dict(data['geometry'])
        aperture = Aperture.from_dict(data['aperture'])
        return cls(geometry=geometry, aperture=aperture)
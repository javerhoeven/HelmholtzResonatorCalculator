from .geometry import Geometry
from .aperture import Aperture

class Resonator:
    """
    Combines a geometry and an aperture to define a Helmholtz resonator.

    This class acts as a simple data container bundling both a cavity (geometry)
    and an acoustic opening (aperture).

    Attributes:
        geometry (Geometry): The internal volume of the resonator.
        aperture (Aperture): The acoustic aperture (tube or slit).
    """

    def __init__(self, geometry: Geometry, aperture: Aperture):
        """
        Initializes a Resonator from a given Geometry and Aperture.

        Args:
            geometry (Geometry): Geometry object representing the resonator's internal shape.
            aperture (Aperture): Aperture object defining the acoustic opening.
        """
        self.geometry = geometry
        self.aperture = aperture

    def to_dict(self) -> dict:
        """
        Serializes the Resonator instance into a dictionary format.

        Returns:
            dict: A dictionary containing serialized geometry and aperture information.
        """
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
    def from_dict(cls, data: dict) -> 'Resonator':
        """
        Reconstructs a Resonator instance from a dictionary representation.

        Args:
            data (dict): Dictionary with 'geometry' and 'aperture' keys.

        Returns:
            Resonator: A new Resonator object with loaded parameters.
        """
        geometry = Geometry.from_dict(data['geometry'])
        aperture = Aperture.from_dict(data['aperture'])
        return cls(geometry=geometry, aperture=aperture)

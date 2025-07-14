from traits.api import HasTraits, Enum, Range, Float, TraitError, Union
from traitsui.api import View, Item, Group
import numpy as np

class Geometry(HasTraits):
    """
    Represents the geometry of a Helmholtz resonator, wich function a acoustic cavity.
    Forms of cylinder and cuboid ar both possible. Calculates and stores the
    volume based on specified shape and dimensions.

    Attributes:
        form (str): Shape of the resonator. Must be either 'cylinder' or 'cuboid'.
        x, y, z (float or None): Dimensions of the cuboid in meters.
        radius, height (float or None): Dimensions of the cylinder in meters.
        volume (float): Calculated volume of the geometry in cubic meters.
    """

    form = Enum('cylinder', 'cuboid')

    # Dimensions for cuboid
    x = Union(None, Float(min=0.001, max=2.0), value=None)
    y = Union(None, Float(min=0.001, max=2.0), value=None)
    z = Union(None, Float(min=0.001, max=2.0), value=None)

    # Dimensions for cylinder
    radius = Union(None, Float(min=0.001, max=1.0), value=None)
    height = Union(None, Float(min=0.001, max=1.0), value=None)

    volume = Float

    def __init__(self, **kwargs):
        """
        Initialize a Geometry instance and compute volume immediately.

        Raises:
            TraitError: If required dimensions are missing or invalid.
        """
        super().__init__(**kwargs)
        self.validate_and_calculate()

    def validate_and_calculate(self):
        """
        Validates input dimensions based on geometry type and calculates volume.

        Raises:
            TraitError: If required parameters are missing or non-positive.
        """
        if self.form == 'cylinder':
            if self.radius is None or self.height is None:
                raise TraitError("Cylinder requires 'radius' and 'height' parameters.")
            if self.radius <= 0 or self.height <= 0:
                raise TraitError("Radius and height must be positive values.")
            self.volume = np.pi * self.radius ** 2 * self.height

        elif self.form == 'cuboid':
            if self.x is None or self.y is None or self.z is None:
                raise TraitError("Cuboid requires all three side lengths x, y, z.")
            if self.x <= 0 or self.y <= 0 or self.z <= 0:
                raise TraitError("x, y und z must be > 0.")
            self.volume = self.x * self.y * self.z

        else:
            raise TraitError("Invalid form, use 'cylinder' or 'cuboid'.")

    def to_dict(self):
        """
        Converts the geometry instance to a dictionary.

        Returns:
            dict: Serialized geometry data including form, dimensions, and volume.
        """
        return {
            "form": self.form,
            "volume": self.volume,
            "radius": getattr(self, "radius", None),
            "height": getattr(self, "height", None),
            "x": getattr(self, "x", None),
            "y": getattr(self, "y", None),
            "z": getattr(self, "z", None)
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Geometry instance from a dictionary.

        Args:
            data (dict): Dictionary containing form and dimension fields.

        Returns:
            Geometry: A new Geometry instance.
        """
        return cls(
            form=data['form'],
            radius=data.get('radius'),
            height=data.get('height'),
            x=data.get('x'),
            y=data.get('y'),
            z=data.get('z')
        )

    # TraitsUI View
    traits_view = View(
        Group(
            Item('form', label="Form"),
            Item('radius', label="Radius (m)", enabled_when='form == "cylinder"'),
            Item('height', label="Höhe (m)", enabled_when='form == "cylinder"'),
            Item('x', label="Länge (m)", enabled_when='form == "cuboid"'),
            Item('y', label="Breite (m)", enabled_when='form == "cuboid"'),
            Item('z', label="Höhe (m)", enabled_when='form == "cuboid"'),
            Item('volume', style='readonly', label="Volumen (m³)"),
        ),
        title="Geometrie",
        buttons=['OK', 'Abbrechen'],
        resizable=True
    )

if __name__ == "__main__":
    geometry = Geometry(form='cylinder', radius=0.1, height=0.5)
    geometry.configure_traits()

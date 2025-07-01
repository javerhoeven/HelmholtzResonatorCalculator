from traits.api import HasTraits, Enum, Range, Float, TraitError
from traitsui.api import View, Item, Group
import numpy as np

class Geometry(HasTraits):
    form = Enum('cylinder', 'cuboid')  # Muss entweder 'cylinder' oder 'cuboid' sein

    # Optional je nach Form
    x = Range(0.001, 2.0, value=None, allow_none=True)
    y = Range(0.001, 2.0, value=None, allow_none=True)
    z = Range(0.001, 2.0, value=None, allow_none=True)
    radius = Range(0.001, 1.0, None, allow_none=True)
    height = Range(0.001, 1.0, None, allow_none=True)

    volume = Float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_and_calculate()

    def validate_and_calculate(self):
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
        """Convert the geometry to a dictionary representation."""
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
        """Creates a Geometry instance from a dictionary"""
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
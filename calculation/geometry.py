import numpy as np

class Geometry():

    def __init__(self,
                 form : str,
                 x : float = None,
                 y : float = None,
                 z : float = None,
                radius : float = None,
                height : float = None,):
        self.form = form

        if form == 'cylinder':
            self.radius = radius
            self.height = height
            if self.radius is None or self.height is None:
                raise ValueError("Cylinder requires 'radius' and 'height' parameters")
            self.volume = np.pi * self.radius **2 *self.height
            
        elif form == 'cuboid':
            self.x = x
            self.y = y
            self.z = z
            if self.x is None or self.y is None or self.z is None:
                raise ValueError("Cuboid requires all three side lengths x, y, z")
            self.volume = self.x*self.y*self.z

        else:
            raise ValueError("Invalid form, use 'cylinder' or 'cuboid'. ")
        

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
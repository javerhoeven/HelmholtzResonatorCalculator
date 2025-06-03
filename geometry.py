import numpy as np

class Geometry():

    def __init__(self,
                 form : str,
                 **kwargs):
        self.form = form

        if form == 'cylinder':
            self.radius = kwargs.get("radius")
            self.height = kwargs.get("height")
            if self.radius is None or self.height is None:
                raise ValueError("Cylinder requires 'radius' and 'height' parameters")
            self.volume = np.pi * self.radius **2 *self.height
            
        elif form == 'cuboid':
            self.x = kwargs.get("x")
            self.y = kwargs.get("y")
            self.z = kwargs.get("z")
            if self.x is None or self.y is None or self.z is None:
                raise ValueError("Cuboid requires all three side lengths x, y, z")
            self.volume = self.x*self.y*self.z

        else:
            raise ValueError("Invalid form, use 'cylinder' or 'cuboid'. ")
        

        
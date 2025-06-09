from geometry import Geometry
from aperture import Aperture

class Resonator():
    def __init__(self, 
                 geometry : Geometry,
                 aperture : Aperture):
        self.geometry = geometry
        self.aperture = aperture
import unittest

from calculation.geometry import Geometry
from calculation.aperture import Aperture
from calculation.medium import Medium

class TestResonator(unittest.TestCase):

    def setup(self):
        self.medium=Medium()
        self.arperture=Aperture()

    # length = Range(0.001, 0.5)  # must be positivev
    # radius = Range(0.005, 1.0, value=None, allow_none=True)  # only for 'tube'
    # width = Range(0.001, 0.5, value=None, allow_none=True)  # only for 'slit'
    # height = Range(0.001, 0.5, value=None, allow_none=True)  # only for 'slit'
    # amount = Range(1, 100, 1)

    # inner_ending = Enum('open', 'flange') # default = 'open'
    # outer_ending = Enum('flange', 'open') # default = 'flange' because it is on the outer wall

    # additional_dampening = Bool(False)
    # xi = Float(None, allow_none=True)  # required, if additional_dampening=True

    # # --- Berechnete Attribute ---
    # area = Float
    # inner_end_correction = Float
    # outer_end_correction = Float





# class Resonator():
#     def __init__(self, 
#                  geometry : Geometry,
#                  aperture : Aperture):
#         self.geometry = geometry
#         self.aperture = aperture

#     def to_dict(self):
#         """Convert the resonator to a dictionary representation."""
#         return {
#             "geometry": self.geometry.to_dict(),
#             "aperture": {
#                 "form": self.aperture.form,
#                 "length": self.aperture.length,
#                 "radius": self.aperture.radius,
#                 "inner_ending": self.aperture.inner_ending,
#                 "outer_ending": self.aperture.outer_ending,
#                 "additional_dampening": self.aperture.additional_dampening,
#                 "xi": self.aperture.xi,
#                 "amount": self.aperture.amount,
#                 "width": self.aperture.width,
#                 "height": self.aperture.height
#             }
#         }
#     @classmethod
#     def from_dict(cls, data):
#         """Creates a Resonator instance from a dictionary"""
#         geometry = Geometry.from_dict(data['geometry'])
#         aperture = Aperture.from_dict(data['aperture'])
#         return cls(geometry=geometry, aperture=aperture)



if __name__ == '__main__':
    unittest.main()
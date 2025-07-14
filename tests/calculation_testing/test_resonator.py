import unittest

from src.calculation.geometry import Geometry
from src.calculation.aperture import Aperture
from src.calculation.medium import Medium

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








if _name_ == '_main_':
    unittest.main()
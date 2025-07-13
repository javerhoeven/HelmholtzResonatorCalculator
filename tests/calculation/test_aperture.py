import unittest
import numpy as np
from calculation import Aperture

class TestApertureEdgeCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.length_min = Aperture.class_traits()['length'].low
        cls.length_max = Aperture.class_traits()['length'].high
        cls.radius_min = Aperture.class_traits()['radius'].low
        cls.radius_max = Aperture.class_traits()['radius'].high
        cls.amount_min = Aperture.class_traits()['amount'].low
        cls.amount_max = Aperture.class_traits()['amount'].high

        cls.length_mid = (cls.length_min + cls.length_max) / 2
        cls.radius_mid = (cls.radius_min + cls.radius_max) / 2
        cls.amount_mid = round((cls.amount_min + cls.amount_max) / 2)

    # -----------------------------------
    # radius = min, amount = min
    # -----------------------------------
    def test_radius_min_amount_min(self):
        a = Aperture(
            form="tube",
            radius=self.radius_min,
            length=self.length_mid,
            amount=self.amount_min,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_min, places=5)

    # -----------------------------------
    # radius = max, amount = max
    # -----------------------------------
    def test_radius_max_amount_max(self):
        a = Aperture(
            form="tube",
            radius=self.radius_max,
            length=self.length_mid,
            amount=self.amount_max,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_max, places=5)

    # -----------------------------------
    # radius = min, amount = mid
    # -----------------------------------
    def test_radius_min_amount_mid(self):
        a = Aperture(
            form="tube",
            radius=self.radius_min,
            length=self.length_mid,
            amount=self.amount_mid,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_min, places=5)

    # -----------------------------------
    # radius = max, amount = mid
    # -----------------------------------
    def test_radius_max_amount_mid(self):
        a = Aperture(
            form="tube",
            radius=self.radius_max,
            length=self.length_mid,
            amount=self.amount_mid,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_max, places=5)

    # -----------------------------------
    # radius = mid, amount = min
    # -----------------------------------
    def test_radius_mid_amount_min(self):
        a = Aperture(
            form="tube",
            radius=self.radius_mid,
            length=self.length_mid,
            amount=self.amount_min,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_mid, places=5)

    # -----------------------------------
    # radius = mid, amount = max
    # -----------------------------------
    def test_radius_mid_amount_max(self):
        a = Aperture(
            form="tube",
            radius=self.radius_mid,
            length=self.length_mid,
            amount=self.amount_max,
            inner_ending='open',
            outer_ending='open'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_mid, places=5)



#same tests with both openings flange

 # -----------------------------------
    # radius = min, amount = min 
    # -----------------------------------
    def test_radius_min_amount_min_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_min,
            length=self.length_mid,
            amount=self.amount_min,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_min, places=5)

    # -----------------------------------
    # radius = max, amount = max
    # -----------------------------------
    def test_radius_max_amount_max_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_max,
            length=self.length_mid,
            amount=self.amount_max,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_max, places=5)

    # -----------------------------------
    # radius = min, amount = mid
    # -----------------------------------
    def test_radius_min_amount_mid_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_min,
            length=self.length_mid,
            amount=self.amount_mid,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_min, places=5)

    # -----------------------------------
    # radius = max, amount = mid
    # -----------------------------------
    def test_radius_max_amount_mid_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_max,
            length=self.length_mid,
            amount=self.amount_mid,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_max, places=5)

    # -----------------------------------
    # radius = mid, amount = min
    # -----------------------------------
    def test_radius_mid_amount_min_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_mid,
            length=self.length_mid,
            amount=self.amount_min,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_mid, places=5)

    # -----------------------------------
    # radius = mid, amount = max
    # -----------------------------------
    def test_radius_mid_amount_max_flange(self):
        a = Aperture(
            form="tube",
            radius=self.radius_mid,
            length=self.length_mid,
            amount=self.amount_max,
            inner_ending='flange',
            outer_ending='flange'
        )

        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_mid, places=5)





    # ---------------------------
    # BLOCK 1: inner=flange, outer=open
    # ---------------------------

    def test_radius_min_amount_min_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_min, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_min, places=5)

    def test_radius_max_amount_max_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_max, length=self.length_mid, amount=self.amount_max, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_max, places=5)

    def test_radius_min_amount_mid_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_mid, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_min, places=5)

    def test_radius_max_amount_mid_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_max, length=self.length_mid, amount=self.amount_mid, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_max, places=5)

    def test_radius_mid_amount_min_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_min, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_mid, places=5)

    def test_radius_mid_amount_max_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_max, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_mid, places=5)

    def test_radius_mid_amount_mid_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_mid, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_mid, places=5)

    def test_radius_min_amount_max_flange_open(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_max, inner_ending='flange', outer_ending='open')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.85 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.6 * self.radius_min, places=5)

    # ---------------------------
    # BLOCK 2: inner=open, outer=flange
    # ---------------------------

    def test_radius_min_amount_min_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_min, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_min, places=5)

    def test_radius_max_amount_max_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_max, length=self.length_mid, amount=self.amount_max, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_max, places=5)

    def test_radius_min_amount_mid_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_mid, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_min, places=5)

    def test_radius_max_amount_mid_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_max, length=self.length_mid, amount=self.amount_mid, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_max**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_max, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_max, places=5)

    def test_radius_mid_amount_min_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_min, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_min, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_mid, places=5)

    def test_radius_mid_amount_max_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_max, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_mid, places=5)

    def test_radius_mid_amount_mid_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_mid, length=self.length_mid, amount=self.amount_mid, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_mid**2 * self.amount_mid, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_mid, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_mid, places=5)

    def test_radius_min_amount_max_open_flange(self):
        a = Aperture(form="tube", radius=self.radius_min, length=self.length_mid, amount=self.amount_max, inner_ending='open', outer_ending='flange')
        self.assertAlmostEqual(a.area, np.pi * self.radius_min**2 * self.amount_max, places=5)
        self.assertAlmostEqual(a.inner_end_correction, 0.6 * self.radius_min, places=5)
        self.assertAlmostEqual(a.outer_end_correction, 0.85 * self.radius_min, places=5)
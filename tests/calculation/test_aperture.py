from calculation.aperture import Aperture
from math import pi

import unittest
import numpy as np

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



class TestApertureEdgeCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Hier werden die min und max-werte von length radius width heigth und amount ermittelt welche man für die edge cases und false cases benötigt.
           Außerdem werden jeweils die Mittelwerte ermittelt.
        """
        #---Minimal-/Maximalwert length---
        cls.length_min = Aperture.class_traits()['length'].handler._low
        cls.length_max = Aperture.class_traits()['length'].handler._high
        #---Minimal-/Maximalwert radius---
        cls.radius_min = Aperture.class_traits()['radius'].handler._low
        cls.radius_max = Aperture.class_traits()['radius'].handler._high
        #---Minimal-/Maximalwert width---
        cls.width_min = Aperture.class_traits()['width'].handler._low
        cls.width_max = Aperture.class_traits()['width'].handler._high
        #---Minimal-/Maximalwert heigth---
        cls.height_min = Aperture.class_traits()['height'].handler._low
        cls.height_max = Aperture.class_traits()['height'].handler._high
        #---Minimal-/Maximalwert amount---
        cls.amount_min = Aperture.class_traits()['amount'].handler._low
        cls.amount_max = Aperture.class_traits()['amount'].handler._high

        #---Mittelwer length---
        cls.length_mid  = (cls.length_min  + cls.length_max) / 2

        #---Mittelwert radius---
        cls.radius_mid  = (cls.radius_min  + cls.radius_max) / 2

        #---Mittelwert width---
        cls.width_mid   = (cls.width_min   + cls.width_max)  / 2

        #---Mittelwer heigth---
        cls.height_mid  = (cls.height_min  + cls.height_max) / 2

        #---Mittelwer heigth gerundet auf eine ganze Zahl---
        cls.amount_mid = round((cls.amount_min + cls.amount_max)/2)

    # ------------------------------------------------------------
    # Hilfsfunktion für gemeinsame Assertions
    # ------------------------------------------------------------
    def _check_tube(self, length, radius, amount):
        ap = Aperture(
            form="tube",
            length=length,
            radius=radius,
            amount=amount,
            inner_ending="open",
            outer_ending="flange",
        )
        # Fläche
        self.assertAlmostEqual(ap.area, amount * pi * radius**2, places=7)
        # Endkorrekturen
        self.assertAlmostEqual(ap.inner_end_correction, 0.6 * radius, places=7)
        self.assertAlmostEqual(ap.outer_end_correction, 0.85 * radius, places=7)

    # ------------------- MIN‑Edge‑Cases --------------------------
    def test_min_length(self):
        self._check_tube(self.length_min, self.radius_mid, self.amount_mid)

    def test_min_radius(self):
        self._check_tube(self.length_mid, self.radius_min, self.amount_mid)

    def test_min_amount(self):
        self._check_tube(self.length_mid, self.radius_mid, self.amount_min)

    # ------------------- MAX‑Edge‑Cases --------------------------
    def test_max_length(self):
        self._check_tube(self.length_max, self.radius_mid, self.amount_mid)

    def test_max_radius(self):
        self._check_tube(self.length_mid, self.radius_max, self.amount_mid)

    def test_max_amount(self):
        self._check_tube(self.length_mid, self.radius_mid, self.amount_max)


   

    # def _slit_correction():
    #     delta_l_a =  2/(3*pi) * (beta + (1- (1+beta**2)**(3/2)) / beta**2 ) + (2/pi) * (1/beta * np.log(beta+np.sqrt(1+beta**2)) + np.log(1/beta*(1+np.sqrt(1+beta**2))))
    #     delta_l = delta_l_a * a
    

    # ---------------- Slit‑Edge‑Cases ohne Schleifen --------------
    # def test_slit_end_correction_min_width_min_height(self):
    #     width, height = self.width_min, self.height_min
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=width, height=height, amount=self.amount_mid)
    #     expected = self._slit_correction(width, height)
    #     self.assertAlmostEqual(ap.inner_end_correction, expected, places=7)
    #     self.assertAlmostEqual(ap.outer_end_correction, expected, places=7)

    # def test_slit_end_correction_min_width_mid_height(self):
    #     width, height = self.width_min, self.height_mid
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=width, height=height, amount=self.amount_mid)
    #     expected = self._slit_correction(width, height)
    #     self.assertAlmostEqual(ap.inner_end_correction, expected, places=7)
    #     self.assertAlmostEqual(ap.outer_end_correction, expected, places=7)

    # def test_slit_end_correction_mid_width_min_height(self):
    #     width, height = self.width_mid, self.height_min
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=width, height=height, amount=self.amount_mid)
    #     expected = self._slit_correction(width, height)
    #     self.assertAlmostEqual(ap.inner_end_correction, expected, places=7)
    #     self.assertAlmostEqual(ap.outer_end_correction, expected, places=7)

    # def test_slit_end_correction_max_width_max_height(self):
    #     width, height = self.width_max, self.height_max
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=width, height=height, amount=self.amount_mid)
    #     expected = self._slit_correction(width, height)
    #     self.assertAlmostEqual(ap.inner_end_correction, expected, places=7)
    #     self.assertAlmostEqual(ap.outer_end_correction, expected, places=7)

    # def test_slit_end_correction_mid_width_mid_height(self):
    #     width, height = self.width_mid, self.height_mid
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=width, height=height, amount=self.amount_mid)
    #     expected = self._slit_correction(width, height)
    #     self.assertAlmostEqual(ap.inner_end_correction, expected, places=7)
    #     self.assertAlmostEqual(ap.outer_end_correction, expected, places=7)

    # def test_slit_end_correction_symmetry(self):
    #     w1, h1 = self.width_min, self.height_max
    #     ap = Aperture(form='slit', length=self.length_mid,
    #                   width=w1, height=h1, amount=self.amount_mid)
    #     c1 = self._slit_correction(w1, h1)
    #     c2 = self._slit_correction(h1, w1)   # Seiten vertauscht
    #     self.assertAlmostEqual(c1, c2, places=9)

    
    
    

if __name__ == '__main__':
    unittest.main()

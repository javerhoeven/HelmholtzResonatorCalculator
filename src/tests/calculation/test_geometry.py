import unittest
from traits.api import TraitError
from traits.trait_types import Float as CheckFloat

from calculation import Geometry
import numpy as np

class TestGeometry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cuboid trait limits
        for axis in ['x', 'y', 'z']:
            trait_handler = Geometry.class_traits()[axis].handler

            for inner_trait in trait_handler.inner_traits():
                if isinstance(inner_trait.handler, CheckFloat):
                    setattr(cls, f"{axis}_min", inner_trait.handler.min)
                    setattr(cls, f"{axis}_max", inner_trait.handler.max)


        # Cylinder trait limits
        translation = {'r' : 'radius',
                       'h' : 'height'}
        for param in translation:
            trait_handler = Geometry.class_traits()[translation[param]].handler

            for inner_trait in trait_handler.inner_traits():
                if isinstance(inner_trait.handler, CheckFloat):
                    setattr(cls, f"{param}_min", inner_trait.handler.min)
                    setattr(cls, f"{param}_max", inner_trait.handler.max)

        # cls.r_min = Geometry.class_traits()['radius'].handler._low
        # cls.r_max = Geometry.class_traits()['radius'].handler._high
        # cls.h_min = Geometry.class_traits()['height'].handler._low
        # cls.h_max = Geometry.class_traits()['height'].handler._high

        # Midpoints
        cls.x_mid = (cls.x_min + cls.x_max) / 2
        cls.y_mid = (cls.y_min + cls.y_max) / 2
        cls.z_mid = (cls.z_min + cls.z_max) / 2
        cls.r_mid = (cls.r_min + cls.r_max) / 2
        cls.h_mid = (cls.h_min + cls.h_max) / 2

    # ---------- Cuboid Tests ----------
    def test_cuboid_mid_values(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_mid, y=self.y_mid, z=self.z_mid).volume,
            self.x_mid * self.y_mid * self.z_mid,
            places=5
        )

    def test_cuboid_min_values(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_min, y=self.y_min, z=self.z_min).volume,
            self.x_min * self.y_min * self.z_min,
            places=5
        )

    def test_cuboid_max_values(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_max, y=self.y_max, z=self.z_max).volume,
            self.x_max * self.y_max * self.z_max,
            places=5
        )

    def test_cuboid_x_min(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_min, y=self.y_mid, z=self.z_mid).volume,
            self.x_min * self.y_mid * self.z_mid,
            places=5
        )

    def test_cuboid_x_max(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_max, y=self.y_mid, z=self.z_mid).volume,
            self.x_max * self.y_mid * self.z_mid,
            places=5
        )

    def test_cuboid_y_min(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_mid, y=self.y_min, z=self.z_mid).volume,
            self.x_mid * self.y_min * self.z_mid,
            places=5
        )

    def test_cuboid_y_max(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_mid, y=self.y_max, z=self.z_mid).volume,
            self.x_mid * self.y_max * self.z_mid,
            places=5
        )

    def test_cuboid_z_min(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_mid, y=self.y_mid, z=self.z_min).volume,
            self.x_mid * self.y_mid * self.z_min,
            places=5
        )

    def test_cuboid_z_max(self):
        self.assertAlmostEqual(
            Geometry(form="cuboid", x=self.x_mid, y=self.y_mid, z=self.z_max).volume,
            self.x_mid * self.y_mid * self.z_max,
            places=5
        )

    # ---------- Cylinder Tests ----------
    def test_cylinder_mid_values(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_mid, height=self.h_mid).volume,
            np.pi * self.r_mid**2 * self.h_mid,
            places=5
        )

    def test_cylinder_min_values(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_min, height=self.h_min).volume,
            np.pi * self.r_min**2 * self.h_min,
            places=5
        )

    def test_cylinder_max_values(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_max, height=self.h_max).volume,
            np.pi * self.r_max**2 * self.h_max,
            places=5
        )

    def test_cylinder_radius_min(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_min, height=self.h_mid).volume,
            np.pi * self.r_min**2 * self.h_mid,
            places=5
        )

    def test_cylinder_radius_max(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_max, height=self.h_mid).volume,
            np.pi * self.r_max**2 * self.h_mid,
            places=5
        )

    def test_cylinder_height_min(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_mid, height=self.h_min).volume,
            np.pi * self.r_mid**2 * self.h_min,
            places=5
        )

    def test_cylinder_height_max(self):
        self.assertAlmostEqual(
            Geometry(form="cylinder", radius=self.r_mid, height=self.h_max).volume,
            np.pi * self.r_mid**2 * self.h_max,
            places=5
        )

    # ---------- Trait Error Tests ----------
    def test_x_toosmall(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_min - 0.001, y=self.y_min, z=self.z_min)

    # def test_x_too_large_raises(self):
    #     with self.assertRaises(TraitError):
    #         Geometry(form='cuboid', x=self.x_max + 0.001, y=self.y_min, z=self.z_min)

    def test_y_toosmall(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_min, y=self.y_min - 0.001, z=self.z_min)

    # def test_y_too_large_raises(self):
    #     with self.assertRaises(TraitError):
    #         Geometry(form='cuboid', x=self.x_min, y=self.y_max + 0.001, z=self.z_min)

    def test_z_toosmall(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_min, y=self.y_min, z=self.z_min - 0.001)

    # def test_z_too_large_trait_error(self):
    #     with self.assertRaises(TraitError):
    #         Geometry(form='cuboid', x=self.x_max, y=self.y_max, z=self.z_max + 0.001)

    def test_radius_toosmall(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder', radius=self.r_min - 0.001, height=self.h_mid)

    # def test_radius_toolarge(self):
    #     with self.assertRaises(TraitError):
    #         Geometry(form='cylinder', radius=self.r_max + 0.001, height=self.h_mid)

    def test_height_toosmall(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder', radius=self.r_mid, height=self.h_min - 0.001)

    # def test_height_toolarge(self):
    #     with self.assertRaises(TraitError):
    #         Geometry(form='cylinder', radius=self.r_mid, height=self.h_max + 0.001)

    def test_false_datatype_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(form=False, x=self.x_min, y=self.y_max, z=self.z_min)

    def test_cuboid_x_zero(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=0, y=self.y_mid, z=self.z_mid)

    def test_cuboid_y_zero(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_mid, y=0, z=self.z_mid)

    def test_cuboid_z_zero(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_mid, y=self.y_mid, z=0)

    def test_cylinder_radius_zero(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder', radius=0, height=self.h_mid)

    def test_cylinder_height_zero(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder', radius=self.r_mid, height=0)

    def test_cylinder_with_xyz_parameters(self):
        with self.assertRaises(TraitError):
            Geometry(form="cylinder", x=self.x_mid, y=self.y_mid, z=self.z_mid)

    def test_cuboid_with_radius_height(self):
        with self.assertRaises(TraitError):
            Geometry(form="cuboid", radius=self.r_mid, height=self.h_mid)

if __name__ == '__main__':
    unittest.main()

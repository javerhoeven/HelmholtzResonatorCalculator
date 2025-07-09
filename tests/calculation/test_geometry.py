import unittest
from traits.api import TraitError
from calculation.geometry import Geometry

class TestGeometry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.x_min = Geometry.class_traits()['x'].handler._low
        cls.x_max = Geometry.class_traits()['x'].handler._high
        cls.y_min = Geometry.class_traits()['y'].handler._low
        cls.y_max = Geometry.class_traits()['y'].handler._high
        cls.z_min = Geometry.class_traits()['z'].handler._low
        cls.z_max = Geometry.class_traits()['z'].handler._high

        cls.x_mid = (cls.x_min + cls.x_max) / 2
        cls.y_mid = (cls.y_min + cls.y_max) / 2
        cls.z_mid = (cls.z_min + cls.z_max) / 2




    # def test_edge_xlow(self):
         
    #      with self

        

    """ 
    fals-value-test
    
    following test check, if values that deviate slightly from min/ max values, trigger trait errors."""
    def test_x_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_min-0.001,  y=self.y_min, z=self.z_min)

    def test_x_too_large_raises(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_max+0.001,y=self.y_min, z=self.z_min)
    
    def test_y_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_min,y=self.y_min-0.001, z=self.z_min)
            

    def test_y_too_large_raises(self):
        
        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_min,y=self.y_max+0.001, z=self.z_min)
    
    def test_z_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid', y=self.y_min,x=self.x_min,z=self.z_min-0.001)
        

    def test_z_too_large_trait_error(self):
       
        with self.assertRaises(TraitError):
            Geometry(form='cuboid', x=self.x_max, y=self.y_max, z=self.z_max+0.001)

    def test_false_geometry_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder',x=self.x_min,y=self.y_min, z=self.z_min)

    def test_missing_datatype_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(x=self.x_min,y=self.x_max,z=self.z_min)
    
    def test_false_datatype_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(form=False,x=self.x_min,y=self.y_max,z=self.z_min)


    """EDGE_Cases"""
    def test_edge_xyz_lower(self):
 
        self.assertAlmostEqual(Geometry(form="cylinder",x=self.x_min,y=self.y_min,z=self.z_min).volume,self.x_min * self.y_min * self.z_min)

    def test_edge_xyz_higher(self):
     
        self.assertAlmostEqual(Geometry(form="cylinder",x=self.x_max,y=self.y_max,z=self.z_max).volume,self.x_min * self.y_max * self.z_max)


    """positive tests with average vallues"""
    def test_edge_xyz_mid(self):

        self.assertAlmostEqual(Geometry(form="cylinder",x=self.x_mid,y=self.y_mid,z=self.z_mid).volume,self.x_min * self.y_max * self.z_max)


#TODO: selbe tests nur mit cuboid


if __name__ == '__main__':
    unittest.main()
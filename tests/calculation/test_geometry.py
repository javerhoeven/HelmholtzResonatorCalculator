import unittest
from traits.api import TraitError
from calculation.geometry import Geometry

class TestGeometry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.x_min = Geometry.class_traits()['x'].low
        cls.x_max = Geometry.class_traits()['x'].high
        cls.y_min = Geometry.class_traits()['y'].low
        cls.y_min = Geometry.class_traits()['y'].high
        cls.z_min = Geometry.class_traits()['z'].low
        cls.z_max = Geometry.class_traits()['z'].high

        cls.x_mid = (cls.x_min + cls.x_max) / 2
        cls.y_mid = (cls.y_min + cls.y_max) / 2
        cls.z_mid = (cls.z_min + cls.z_max) / 2




    def test_edge_xlow(self):
         
         with self

        

    """ 
    fals-value-test
    
    following test check, if values that deviate slightly from min/ max values, trigger trait errors."""
    def test_x_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.xmin-0.001,  y=self.y_min, z=self.z_min)

    def test_x_too_large_raises(self):
        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_max+0.001,y=self.y_min, z=self.z_min)
    
    def test_y_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.xmin,y=self.ymin-0.001, , z=self.z_min)
            

    def test_y_too_large_raises(self):
        
        with self.assertRaises(TraitError):
            Geometry(form='cuboid',x=self.x_min,y=self.y_max+0.001, z=self.z_min)
    
        def test_z_toosmall(self):

        with self.assertRaises(TraitError):
            Geometry(form='cuboid', y=self.y_min,x=self.xmin,z=self.zmin-0.001)
            

    def test_z_too_large_trait_error(self):
       
        with self.assertRaises(TraitError):
            Geometry(Geometry(form='', x=self.x_max,y=self.y_max,z=self.z_max+0.001))

    def test_false_geometry_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(form='cylinder',x=self.x_min,y=self.y_min, z=self.z_min)

    def test_missing_datatype_trait_error(self):
        with self.assertRaises(TraitError):
            Geometry(x=self.xmin,y=self.xmax,z=self.z_min)
    
    def test_false_datatype_trait_error
        with self.assertRaises(TraitError):
            Geometry(form=False,x=self.xmin,y=self.ymax,z=self.z_min)


    """EDGE_Cases"""
    def test_edge_xyz-lower(self):
 
        self.assertAlmostEqual(Geometry(formrm="cylinder",x=self.xmin,y=self.ymin,z=self.zmin).volume,self.x_min * self.y_min * self.z_min)

    def test_edge_xyz-higher(self):
     
        self.assertAlmostEqual(Geometry(formrm="cylinder",x=self.xmax,y=self.ymax,z=self.zmax).volume,self.x_min * self.y_max * self.z_max)


    """positive tests with average vallues"""
    def test_edge_xyz_mid

        self.assertAlmostEqual(Geometry(formrm="cylinder",x=self.xmid,y=self.ymid,z=self.zmid).volume,self.x_min * self.y_max * self.z_max)


#TODO: selbe tests nur mit cuboid
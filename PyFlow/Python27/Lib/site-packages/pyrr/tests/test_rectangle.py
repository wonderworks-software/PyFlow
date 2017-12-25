try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import rectangle


class test_rectangle(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.rectangle
        from pyrr import rectangle

    def test_create(self):
        result = rectangle.create()
        np.testing.assert_almost_equal(result, [[0,0],[1,1]], decimal=5)

    def test_create_dtype(self):
        result = rectangle.create(dtype=np.float)
        np.testing.assert_almost_equal(result, [[0.,0.],[1.,1.]], decimal=5)

    def test_create_zeros(self):
        result = rectangle.create_zeros()
        np.testing.assert_almost_equal(result, [[0,0],[0,0]], decimal=5)

    def test_create_from_bounds(self):
        result = rectangle.create_from_bounds(-1, 1, -2, 2)
        np.testing.assert_almost_equal(result, [[-1,-2],[2,4]], decimal=5)

    def test_bounds(self):
        rect = rectangle.create_from_bounds(-1, 1, -2, 2)
        result = rectangle.bounds(rect)
        np.testing.assert_almost_equal(result, (-1,1,-2,2), decimal=5)

    def test_scale_by_vector(self):
        result = rectangle.scale_by_vector([[-1.,-2.],[2.,4.]], [2.,3.])
        np.testing.assert_almost_equal(result, [[-2.,-6.],[4.,12.]], decimal=5)

    def test_scale_by_vector3(self):
        result = rectangle.scale_by_vector([[-1.,-2.],[2.,4.]], [2.,3.,4.])
        np.testing.assert_almost_equal(result, [[-2.,-6.],[4.,12.]], decimal=5)

    def test_right(self):
        result = rectangle.right([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_right_negative(self):
        result = rectangle.right([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_left(self):
        result = rectangle.left([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_left_negative(self):
        result = rectangle.left([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, -2., decimal=5)

    def test_top(self):
        result = rectangle.top([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 6., decimal=5)

    def test_top_negative(self):
        result = rectangle.top([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_bottom(self):
        result = rectangle.bottom([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_bottom_negative(self):
        result = rectangle.bottom([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, -2., decimal=5)

    def test_x(self):
        result = rectangle.x([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_x_negative(self):
        result = rectangle.x([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_y(self):
        result = rectangle.y([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_y_negative(self):
        result = rectangle.y([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_width(self):
        result = rectangle.width([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 3., decimal=5)

    def test_width_negative(self):
        result = rectangle.width([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, -3., decimal=5)

    def test_height(self):
        result = rectangle.height([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_height_negative(self):
        result = rectangle.height([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, -4., decimal=5)

    def test_abs_height(self):
        result = rectangle.abs_height([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_abs_height_negative(self):
        result = rectangle.abs_height([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_abs_width(self):
        result = rectangle.abs_width([[1.,2.],[3.,4.]])
        np.testing.assert_almost_equal(result, 3., decimal=5)

    def test_abs_width_negative(self):
        result = rectangle.abs_width([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, 3., decimal=5)

    def test_position(self):
        result = rectangle.position([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, [1.,2.], decimal=5)

    def test_size(self):
        result = rectangle.size([[1.,2.],[-3.,-4.]])
        np.testing.assert_almost_equal(result, [-3.,-4.], decimal=5)

    
if __name__ == '__main__':
    unittest.main()

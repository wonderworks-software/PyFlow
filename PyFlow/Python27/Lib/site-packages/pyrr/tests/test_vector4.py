try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import vector4


class test_vector4(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.vector4
        from pyrr import vector4

    def test_create(self):
        result = vector4.create()
        np.testing.assert_almost_equal(result, [0.,0.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_values(self):
        result = vector4.create(1.,2.,3.,4., dtype=np.float32)
        np.testing.assert_almost_equal(result, [1.,2.,3.,4.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_list(self):
        with self.assertRaises(ValueError):
            vector4.create([1., 2., 3., 4.])

    def test_create_unit_length_x(self):
        result = vector4.create_unit_length_x()
        np.testing.assert_almost_equal(result, [1.,0.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_x_dtype(self):
        result = vector4.create_unit_length_x(dtype=np.float32)
        np.testing.assert_almost_equal(result, [1.,0.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_unit_length_y(self):
        result = vector4.create_unit_length_y()
        np.testing.assert_almost_equal(result, [0.,1.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_y_dtype(self):
        result = vector4.create_unit_length_y(dtype=np.float32)
        np.testing.assert_almost_equal(result, [0.,1.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_unit_length_z(self):
        result = vector4.create_unit_length_z()
        np.testing.assert_almost_equal(result, [0.,0.,1.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_z_dtype(self):
        result = vector4.create_unit_length_z(dtype=np.float32)
        np.testing.assert_almost_equal(result, [0.,0.,1.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_unit_length_w(self):
        result = vector4.create_unit_length_w()
        np.testing.assert_almost_equal(result, [0.,0.,0.,1.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_w_dtype(self):
        result = vector4.create_unit_length_w(dtype=np.float32)
        np.testing.assert_almost_equal(result, [0.,0.,0.,1.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_from_matrix44_translation(self):
        mat = np.array([
            [1.,2.,3.,4.,],
            [5.,6.,7.,8.,],
            [9.,10.,11.,12.,],
            [13.,14.,15.,16.,],
        ])
        result = vector4.create_from_matrix44_translation(mat)
        np.testing.assert_almost_equal(result, [13.,14.,15.,16.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix44_translation_dtype_matches(self):
        mat = np.array([
            [1.,2.,3.,4.,],
            [5.,6.,7.,8.,],
            [9.,10.,11.,12.,],
            [13.,14.,15.,16.,],
        ], dtype=np.float32)
        result = vector4.create_from_matrix44_translation(mat)
        np.testing.assert_almost_equal(result, [13.,14.,15.,16.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_normalize_single_vector(self):
        result = vector4.normalize([1.,1.,1.,1.])
        np.testing.assert_almost_equal(result, [0.5, 0.5, 0.5, 0.5], decimal=5)

    def test_normalize_batch(self):
        result = vector4.normalize([
            [1.,1.,1.,1.],
            [-1.,-1.,-1.,1.],
            [0.,2.,7.,1.],
        ])
        expected = [
            [0.5, 0.5, 0.5, 0.5],
            [-0.5,-0.5,-0.5, 0.5],
            [0., 0.27216553, 0.95257934, 0.13608276],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_squared_length_single_vector(self):
        result = vector4.squared_length([1.,1.,1.,1.])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_squared_length_batch(self):
        result = vector4.squared_length([
            [1.,1.,1.,1.],
            [-1.,-1.,-1.,1.],
            [0.,2.,7.,1.],
        ])
        expected = [
            4.,
            4.,
            54.,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_length(self):
        result = vector4.length([1.,1.,1.,1.])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_length_batch(self):
        result = vector4.length([
            [1.,1.,1.,1.],
            [-1.,-1.,-1.,1.],
            [0.,2.,7.,1.],
        ])
        expected = [
            2.,
            2.,
            7.34846923,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length(self):
        result = vector4.set_length([1.,1.,1.,1.],3.)
        expected = [1.5,1.5,1.5,1.5]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length_batch_vector(self):
        result = vector4.set_length([
            [1.,1.,1.,1.],
            [-1.,-1.,-1.,1.],
            [0.,2.,7.,1.],
            ], 2.0)
        expected = [
            [1.,1.,1.,1.],
            [-1.,-1.,-1.,1.],
            [0., 0.54433105, 1.90515869, 0.27216553],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_dot_adjacent(self):
        result = vector4.dot([1.,0.,0.,1.], [0.,1.,0.,1.])
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_dot_parallel(self):
        result = vector4.dot([0.,1.,0.,1.], [0.,1.,0.,1.])
        np.testing.assert_almost_equal(result, 2.0, decimal=5)

    def test_dot_angle(self):
        result = vector4.dot([.2,.2,0.,1.], [2.,-.2,0.,1.])
        np.testing.assert_almost_equal(result, 1.359999, decimal=5)

    def test_dot_batch(self):
        result = vector4.dot([
            [1.,0.,0.,1.],
            [0.,1.,0.,1.],
            [.2,.2,0.,1.]
        ],[
            [0.,1.,0.,1.],
            [0.,1.,0.,1.],
            [2.,-.2,0.,1.]
        ])
        expected = [
            1.,
            2.,
            1.36
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)


if __name__ == '__main__':
    unittest.main()

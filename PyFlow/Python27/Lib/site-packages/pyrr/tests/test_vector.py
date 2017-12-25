try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import vector, vector3, vector4


class test_vector(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.vector
        from pyrr import vector

    def test_normalize_single_vector(self):
        result = vector3.normalize([1.,1.,1.])
        np.testing.assert_almost_equal(result, [0.57735, 0.57735, 0.57735], decimal=5)

    def test_normalize_batch(self):
        result = vector3.normalize([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            [0.57735, 0.57735, 0.57735],
            [-0.57735,-0.57735,-0.57735],
            [0., 0.274721, 0.961524],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_squared_length_single_vector(self):
        result = vector3.squared_length([1.,1.,1.])
        np.testing.assert_almost_equal(result, 3., decimal=5)

    def test_squared_length_batch(self):
        result = vector3.squared_length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            3.,
            3.,
            53.,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_length_vector3(self):
        result = vector3.length([1.,1.,1.])
        np.testing.assert_almost_equal(result, 1.73205, decimal=5)

    def test_length_vector4(self):
        result = vector3.length([1.,1.,1.,1.])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_length_vector3_batch(self):
        result = vector3.length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            1.73205,
            1.73205,
            7.28011,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length_vector3(self):
        result = vector3.set_length([1.,1.,1.],2.)
        expected = [1.15470,1.15470,1.15470]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length_vector4(self):
        result = vector4.set_length([1.,1.,1.,1.],2.)
        expected = [1.,1.,1.,1.]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length_batch_vector(self):
        result = vector3.set_length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
            ], 2.0)
        expected = [
            [1.15470,1.15470,1.15470],
            [-1.15470,-1.15470,-1.15470],
            [0.,0.54944,1.92304],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_dot_adjacent(self):
        result = vector3.dot([1.,0.,0.], [0.,1.,0.])
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_dot_parallel(self):
        result = vector3.dot([0.,1.,0.], [0.,1.,0.])
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_dot_angle(self):
        result = vector3.dot([.2,.2,0.], [2.,-.2,0.])
        np.testing.assert_almost_equal(result, 0.36, decimal=5)

    def test_dot_batch(self):
        result = vector3.dot([
            [1.,0.,0.],
            [0.,1.,0.],
            [.2,.2,0.]
        ],[
            [0.,1.,0.],
            [0.,1.,0.],
            [2.,-.2,0.]
        ])
        expected = [0.,1.,0.36]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_interoplation(self):
        result = vector3.interpolate([0.,0.,0.], [1.,1.,1.], 0.5)
        np.testing.assert_almost_equal(result, [.5,.5,.5], decimal=5)

        result = vector3.interpolate([0.,0.,0.], [2.,2.,2.], 0.5)
        np.testing.assert_almost_equal(result, [1.,1.,1.], decimal=5)

if __name__ == '__main__':
    unittest.main()

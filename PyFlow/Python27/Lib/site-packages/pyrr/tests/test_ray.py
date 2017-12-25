try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import ray


class test_ray(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.ray
        from pyrr import ray

    def test_create(self):
        result = ray.create([0.,0.,0.],[0.,0.,1.])
        np.testing.assert_almost_equal(result, [[0.,0.,0.],[0.,0.,1.]], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_dtype(self):
        result = ray.create([0,0,0],[0,0,1], dtype=np.int)
        np.testing.assert_almost_equal(result, [[0,0,0],[0,0,1]], decimal=5)
        self.assertTrue(result.dtype == np.int)

    def test_create_from_line(self):
        result = ray.create_from_line([
            [0.,10.,0.],
            [10.,10.,0.]
        ])
        np.testing.assert_almost_equal(result, [[0.,10.,0.],[1.,0.,0.]], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_invert(self):
        result = ray.invert([[0.,10.,0.],[1.,0.,0.]])
        np.testing.assert_almost_equal(result, [[0.,10.,0.],[-1.,0.,0.]], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_position(self):
        result = ray.position([[0.,10.,0.],[1.,0.,0.]])
        np.testing.assert_almost_equal(result, [0.,10.,0.], decimal=5)

    def test_direction(self):
        result = ray.direction([[0.,10.,0.],[1.,0.,0.]])
        np.testing.assert_almost_equal(result, [1.,0.,0.], decimal=5)


if __name__ == '__main__':
    unittest.main()


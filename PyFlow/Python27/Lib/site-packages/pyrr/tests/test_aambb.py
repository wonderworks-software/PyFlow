try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import aambb
from pyrr import aabb
from pyrr import vector


class test_aambb(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.aambb
        from pyrr import aambb

    def test_create_zeros(self):
        result = aambb.create_zeros()
        self.assertTrue(np.array_equal(result, [[0.,0.,0.],[0.,0.,0.]]))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_create_from_bounds(self):
        bounds = [[-1.,1.,-1.], [2.,1.,0.]]
        result = aambb.create_from_bounds(*bounds)
        length = max(vector.length(bounds[0]), vector.length(bounds[1]))
        self.assertTrue(np.array_equal(result, [[-length,-length,-length],[length,length,length]]))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_create_from_points(self):
        result = aambb.create_from_points(np.array([[-1.0, 0.0, 0.0]]))
        self.assertTrue(np.array_equal(result, [[-1.0,-1.0,-1.0],[ 1.0, 1.0, 1.0]]))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_center_point(self):
        # this should always be 0,0,0
        result = aambb.create_from_bounds([-1.,1.,-1.], [2.,1.,0.])
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_create_from_aabbs(self):
        a1 = aambb.create_from_points([
            [ 0.0, 0.0, 0.0],
            [ 1.0, 1.0,-1.0]
        ])
        a2 = aambb.create_from_points([
            [ 0.0, 0.0, 2.0],
            [-1.0,-1.0, 1.0]
        ])
        result = aambb.create_from_aabbs([a1, a2])
        length = np.amax(vector.length([a1, a2]))
        self.assertTrue(np.array_equal(result, [[-length,-length,-length],[length,length,length]]), (result,))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_add_point(self):
        a = aambb.create_from_bounds([-0.5,-0.5,-0.5], [0.5,0.5,0.5])
        points = np.array([
            [ 2.0,-1.0,-1.0],
            [ 1.0, 3.0,-1.0],
        ])
        result = aambb.add_points(a, points)
        length = np.amax(vector.length([a, points]))
        self.assertTrue(np.array_equal(result, [[-length,-length,-length],[length,length,length]]), (result,))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))

    def test_add_aabbs(self):
        a1 = aambb.create_from_bounds([-0.5,-0.5,-0.5], [0.5,0.5,0.5])
        a2 = aambb.create_from_bounds([1.0,-2.0, 1.0], [2.0,-1.0, 1.0])
        result = aambb.add_aabbs(a1, [a2])
        length = np.amax(vector.length([a1, a2]))
        self.assertTrue(np.array_equal(result, [[-length,-length,-length],[length,length,length]]), (result,))
        self.assertTrue(np.array_equal(aambb.centre_point(result), [0.0,0.0,0.0]))


if __name__ == '__main__':
    unittest.main()


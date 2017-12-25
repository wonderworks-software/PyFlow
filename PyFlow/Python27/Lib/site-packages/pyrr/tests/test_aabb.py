try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import aabb


class test_aabb(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.aabb
        from pyrr import aabb

    def test_create_zeros(self):
        result = aabb.create_zeros()
        self.assertTrue(np.array_equal(result, [[0,0,0],[0,0,0]]))

    def test_create_from_bounds(self):
        result = aabb.create_from_bounds([-1,-1,-1],[1,1,1])
        self.assertTrue(np.array_equal(result, [[-1,-1,-1],[1,1,1]]))

    def test_create_from_points(self):
        points = np.array([[-1.0,-1.0,-1.0]])
        result = aabb.create_from_points(points)
        expected = np.array([
                [-1.0,-1.0,-1.0],
                [-1.0,-1.0,-1.0]
        ])
        self.assertTrue(np.array_equal(result, expected))

        points = np.array([
            [-1.0,-1.0,-1.0],
            [-1.0, 2.0,-2.0],
        ])
        result = aabb.create_from_points(points)
        expected = np.array([
            [-1.0,-1.0,-2.0],
            [-1.0, 2.0,-1.0],
        ])
        self.assertTrue(np.array_equal(result, expected))

    def test_create_from_aabbs(self):
        # -1
        a1 = np.array([
            [-1.0, 0.0, 0.0 ],
            [-1.0,-1.0,-1.0 ]
        ])
        # +1
        a2 = np.array([
            [ 1.0,-1.0,-1.0 ],
            [ 1.0, 1.0, 1.0 ]
        ])

        # -1 to +1
        result = aabb.create_from_aabbs(np.array([a1, a2]))
        expected = np.array([
            [-1.0,-1.0,-1.0 ],
            [ 1.0, 1.0, 1.0 ]
        ])

        self.assertTrue(np.array_equal(result, expected))

    def test_add_point(self):
        obj = np.array([
            [-1.0,-1.0,-1.0],
            [-1.0,-1.0,-1.0]
        ])
        points = np.array([1.0, 1.0, 1.0])
        result = aabb.add_points(obj, points)
        expected = np.array([
            [-1.0,-1.0,-1.0 ],
            [ 1.0, 1.0, 1.0 ]
        ])
        self.assertTrue(np.array_equal(result, expected))

    def test_add_aabbs(self):
        a = aabb.create_zeros()

        a1 = np.array([
            [-1.0,-1.0,-1.0],
            [ 1.0, 1.0, 1.0]
        ])
        result = aabb.add_aabbs(a, a1)
        expected = np.array([
            [-1.0,-1.0,-1.0],
            [ 1.0, 1.0, 1.0]
        ])
        self.assertTrue(np.array_equal(result, expected))


        a = np.array([
            [-1.0,-1.0,-1.0],
            [ 1.0, 1.0, 1.0]
        ])
        a2 = np.array([
            [-1.0, 0.0,-1.0],
            [ 2.0, 1.0, 1.0]
        ])
        result = aabb.add_aabbs(a, a2)
        expected = np.array([
            [-1.0,-1.0,-1.0],
            [ 2.0, 1.0, 1.0]
        ])
        self.assertTrue(np.array_equal(result, expected))

    def test_centre_point_single_point(self):
        points = np.array([[-1.0,-1.0,-1.0]])
        obj = aabb.create_from_points(points)
        result = aabb.centre_point(obj)
        expected = np.array([-1.0,-1.0,-1.0])
        self.assertTrue(np.array_equal(result, expected))

    def test_centre_point_multiple_points(self):
        points = np.array([
            [ 1.0, 1.0, 1.0],
            [-1.0,-1.0,-1.0]
        ])
        obj = aabb.create_from_points(points)
        result = aabb.centre_point(obj)
        expected = np.zeros(3)
        self.assertTrue(np.array_equal(result, expected))

    def test_minimum(self):
        a = aabb.create_from_bounds([-1,-1,-1],[1,1,1])
        result = aabb.minimum(a)
        self.assertTrue(np.array_equal(result, [-1,-1,-1]))

    def test_maximum(self):
        a = aabb.create_from_bounds([-1,-1,-1],[1,1,1])
        result = aabb.maximum(a)
        self.assertTrue(np.array_equal(result, [1,1,1]))

    def test_clamp_points_single(self):
        a = aabb.create_from_bounds([-1,-1,-1],[1,1,1])
        points = np.array([2,1,1])
        result = aabb.clamp_points(a, points)
        expected = np.array([1,1,1])
        self.assertTrue(np.array_equal(result, expected))

    def test_clamp_points_list(self):
        a = aabb.create_from_bounds([-1,-1,-1],[1,1,1])
        points = np.array([
            [1,1,1],
            [2,1,1],
            [-1,-1,-1],
            [-2,-2,-2],
        ])
        result = aabb.clamp_points(a, points)
        expected = np.array([[1,1,1],[1,1,1],[-1,-1,-1],[-1,-1,-1]])
        self.assertTrue(np.array_equal(result, expected))

if __name__ == '__main__':
    unittest.main()


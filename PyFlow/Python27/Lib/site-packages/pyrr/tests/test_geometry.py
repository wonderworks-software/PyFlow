try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import geometry

# TODO: test all combinations of st, rgba, and type

class test_geometry(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.geometry
        from pyrr import geometry

    def test_create_quad(self):
        v, i = geometry.create_quad()
        expected_v = np.array([
            [ 0.5, 0.5, 0.],
            [-0.5, 0.5, 0.],
            [-0.5,-0.5, 0.],
            [ 0.5,-0.5, 0.],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_quad_scale(self):
        v, i = geometry.create_quad((2.0,0.5))
        expected_v = np.array([
            [ 1., 0.25, 0.],
            [-1., 0.25, 0.],
            [-1.,-0.25, 0.],
            [ 1.,-0.25, 0.],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_quad_st(self):
        v, i = geometry.create_quad(st=True)
        expected_v = np.array([
            [ 0.5, 0.5, 0., 1., 1.],
            [-0.5, 0.5, 0., 0., 1.],
            [-0.5,-0.5, 0., 0., 0.],
            [ 0.5,-0.5, 0., 1., 0.],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_quad_st_values(self):
        v, i = geometry.create_quad(st=((0.1,0.2),(0.3,0.4)))
        expected_v = np.array([
            [ 0.5, 0.5, 0., 0.3, 0.4],
            [-0.5, 0.5, 0., 0.1, 0.4],
            [-0.5,-0.5, 0., 0.1, 0.2],
            [ 0.5,-0.5, 0., 0.3, 0.2],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_quad_rgba(self):
        v, i = geometry.create_quad(rgba=True)
        expected_v = np.array([
            [ 0.5, 0.5, 0., 1., 1., 1., 1.],
            [-0.5, 0.5, 0., 1., 1., 1., 1.],
            [-0.5,-0.5, 0., 1., 1., 1., 1.],
            [ 0.5,-0.5, 0., 1., 1., 1., 1.],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_quad_rgba_values(self):
        v, i = geometry.create_quad(rgba=((0.1,0.2,0.3,0.4),(0.5,0.6,0.7,0.8),(0.9,1.0,1.1,1.2),(1.3,1.4,1.5,1.6)))
        expected_v = np.array([
            [ 0.5, 0.5, 0., .1, .2, .3, .4],
            [-0.5, 0.5, 0., .5, .6, .7, .8],
            [-0.5,-0.5, 0., .9, 1., 1.1, 1.2],
            [ 0.5,-0.5, 0., 1.3, 1.4, 1.5, 1.6],
        ])
        expected_i = np.array([0,1,2,0,2,3])
        self.assertTrue(np.allclose(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i))

    def test_create_cube(self):
        v, i = geometry.create_cube()
        expected_v = np.array([
            [ 0.5,  0.5,  0.5],
            [-0.5,  0.5,  0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5, -0.5],
            [ 0.5,  0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5, -0.5, -0.5],
            [-0.5,  0.5, -0.5],
            [ 0.5,  0.5, -0.5],
            [ 0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [-0.5,  0.5,  0.5],
            [-0.5,  0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5,  0.5, -0.5],
            [-0.5,  0.5, -0.5],
            [-0.5,  0.5,  0.5],
            [ 0.5,  0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [-0.5, -0.5,  0.5],
            [-0.5, -0.5, -0.5],
            [ 0.5, -0.5, -0.5]
        ])
        expected_i = np.array([
            0, 1, 2, 0, 2, 3, 4, 5, 6, 4, 6, 7, 8, 9, 10, 8, 10, 11, 12, 13,
            14, 12, 14, 15, 16, 17, 18, 16, 18, 19, 20, 21, 22, 20, 22, 23
        ])
        self.assertTrue(np.array_equal(v, expected_v), (v,))
        self.assertTrue(np.array_equal(i, expected_i), (i,))

if __name__ == '__main__':
    unittest.main()


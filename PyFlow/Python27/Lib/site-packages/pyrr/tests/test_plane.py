try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import plane

class test_plane(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.plane
        from pyrr import plane

    def test_create(self):
        result = plane.create()
        self.assertTrue(np.allclose(result, [0,0,1,0]))

    def test_create_2(self):
        result = plane.create([1.,0.,0.], 5.)
        self.assertTrue(np.allclose(result, [1.,0.,0.,5.]))

    def test_create_from_points(self):
        vecs = np.array([
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, 1.0, 0.0 ],
            [ 1.0, 1.0, 0.0 ]
        ])
        result = plane.create_from_points(*vecs)
        self.assertTrue(np.allclose(result, [0.,0.,1.,0.]))

    def test_create_from_position(self):
        position = np.array([1.0, 0.0, 0.0])
        normal = np.array([0.0, 3.0, 0.0])
        result = plane.create_from_position(position, normal)
        self.assertTrue(np.allclose(result, [0., 1., 0., 0.]))

    def test_create_xy(self):
        result = plane.create_xy()
        self.assertTrue(np.allclose(result, [0., 0., 1., 0.]))

    def test_create_xy_invert_distance(self):
        result = plane.create_xy(invert=True, distance=2.)
        self.assertTrue(np.allclose(result, [0., 0., -1., 2.]))

    def test_create_xz(self):
        result = plane.create_xz()
        self.assertTrue(np.allclose(result, [0., 1., 0., 0.]))

    def test_create_xz_invert_distance(self):
        result = plane.create_xz(invert=True, distance=2.)
        self.assertTrue(np.allclose(result, [0., -1., 0., 2.]))

    def test_create_yz(self):
        result = plane.create_yz()
        self.assertTrue(np.allclose(result, [1., 0., 0., 0.]))

    def test_create_yz_invert_distance(self):
        result = plane.create_yz(invert=True, distance=2.)
        self.assertTrue(np.allclose(result, [-1., 0., 0., 2.]))

    def test_invert_normal(self):
        p = np.array([1.0, 0.0, 0.0, 1.0])
        result = plane.invert_normal(p)
        self.assertTrue(np.allclose(result, [-1.0, 0.0, 0.0, -1.0]))

    def test_position(self):
        p = plane.create_xz(distance=5.)
        result = plane.position(p)
        self.assertTrue(np.allclose(result, [0.,5.,0.]))

    def test_normal(self):
        p = plane.create_xz(distance=5.)
        result = plane.normal(p)
        self.assertTrue(np.allclose(result, [0.,1.,0.]))

if __name__ == '__main__':
    unittest.main()


try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import line, ray

class test_line(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.line
        from pyrr import line

    def test_create_zeros(self):
        result = line.create_zeros()
        self.assertTrue(np.allclose(result, [[0,0,0],[0,0,0]]))

    def test_create_from_points(self):
        result = line.create_from_points([-1.,0.,0.],[1.,0.,0.])
        self.assertTrue(np.allclose(result, [[-1,0,0],[1,0,0]]))

    def test_create_from_ray(self):
        r = ray.create([0.,0.,0.], [1., 0.,0.])
        result = line.create_from_ray(r)
        self.assertTrue(np.allclose(result, [[0,0,0],[1,0,0]]))

    def test_start(self):
        l = line.create_from_points([-1.,0.,0.],[1.,0.,0.])
        result = line.start(l)
        self.assertTrue(np.allclose(result, [-1,0,0]))

    def test_end(self):
        l = line.create_from_points([-1.,0.,0.],[1.,0.,0.])
        result = line.end(l)
        self.assertTrue(np.allclose(result, [1,0,0]))

if __name__ == '__main__':
    unittest.main()

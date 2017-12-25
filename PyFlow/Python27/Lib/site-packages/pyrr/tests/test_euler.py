try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import euler


class test_euler(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.euler
        from pyrr import euler

    def test_create(self):
        self.assertTrue(np.array_equal(euler.create(), [0., 0., 0.]))
        e = euler.create(roll=1., pitch=2., yaw=3.)
        self.assertEqual(euler.roll(e), 1.)
        self.assertEqual(euler.pitch(e), 2.)
        self.assertEqual(euler.yaw(e), 3.)
        self.assertTrue(np.array_equal(e, [1., 2., 3.]))


if __name__ == '__main__':
    unittest.main()

from __future__ import absolute_import, division, print_function
try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import quaternion, matrix44, matrix33, euler


class test_matrix_quaternion(unittest.TestCase):
    def test_m44_q_equivalence(self):
        """Test for equivalance of matrix and quaternion rotations.

        Create a matrix and quaternion, rotate each by the same values
        then convert matrix<->quaternion and check the results are the same.
        """
        m = matrix44.create_from_x_rotation(np.pi / 2.)
        mq = quaternion.create_from_matrix(m)

        q = quaternion.create_from_x_rotation(np.pi / 2.)
        qm = matrix44.create_from_quaternion(q)

        self.assertTrue(np.allclose(np.dot([1., 0., 0., 1.], m), [1., 0., 0., 1.]))
        self.assertTrue(np.allclose(np.dot([1., 0., 0., 1.], qm), [1., 0., 0., 1.]))

        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0., 1.]), [1., 0., 0., 1.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(mq, [1., 0., 0., 1.]), [1., 0., 0., 1.]))

        np.testing.assert_almost_equal(q, mq, decimal=5)
        np.testing.assert_almost_equal(m, qm, decimal=5)

    def test_euler_equivalence(self):
        eulers = euler.create_from_x_rotation(np.pi / 2.)
        m = matrix33.create_from_x_rotation(np.pi / 2.)
        q = quaternion.create_from_x_rotation(np.pi / 2.)
        qm = matrix33.create_from_quaternion(q)
        em = matrix33.create_from_eulers(eulers)
        self.assertTrue(np.allclose(qm, m))
        self.assertTrue(np.allclose(qm, em))
        self.assertTrue(np.allclose(m, em))

    def test_quaternion_matrix_conversion(self):
        # https://au.mathworks.com/help/robotics/ref/quat2rotm.html?requestedDomain=www.mathworks.com
        q = quaternion.create(0.7071, 0., 0., 0.7071)
        m33 = matrix33.create_from_quaternion(q)
        expected = np.array([
            [1., 0., 0.],
            [0.,-0.,-1.],
            [0., 1.,-0.],
        ])
        self.assertTrue(np.allclose(m33, expected))

        # issue #42
        q = quaternion.create(*[0.80087974, 0.03166748, 0.59114721,-0.09018753])
        m33 = matrix33.create_from_quaternion(q)
        q2 = quaternion.create_from_matrix(m33)
        print(q, q2)
        self.assertTrue(np.allclose(q, q2))

        q3 = quaternion.create_from_matrix(m33.T)
        self.assertFalse(np.allclose(q, q3))



if __name__ == '__main__':
    unittest.main()

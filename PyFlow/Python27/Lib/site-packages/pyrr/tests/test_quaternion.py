#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import quaternion


class test_quaternion(unittest.TestCase):
    # many of these values are taken from searches on wolfram alpha

    def test_import(self):
        import pyrr
        pyrr.quaternion
        from pyrr import quaternion

    def test_create(self):
        result = quaternion.create()
        np.testing.assert_almost_equal(result, [0., 0., 0., 1.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_parameters(self):
        result = quaternion.create(1.0, 2.0, 3.0, 4.0)
        np.testing.assert_almost_equal(result, [1.0, 2.0, 3.0, 4.0], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_x_rotation(self):
        # 180 degree turn around X axis
        q = quaternion.create_from_x_rotation(np.pi)
        self.assertTrue(np.allclose(q, [1., 0., 0., 0.]))

        # 90 degree rotation around X axis
        q = quaternion.create_from_x_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(q, [np.sqrt(0.5), 0., 0., np.sqrt(0.5)]))

        # -90 degree rotation around X axis
        q = quaternion.create_from_x_rotation(-np.pi / 2.)
        self.assertTrue(np.allclose(q, [-np.sqrt(0.5), 0., 0., np.sqrt(0.5)]))

    def test_create_from_y_rotation(self):
        # 180 degree turn around Y axis
        q = quaternion.create_from_y_rotation(np.pi)
        self.assertTrue(np.allclose(q, [0., 1., 0., 0.]))

        # 90 degree rotation around Y axis
        q = quaternion.create_from_y_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(q, [0., np.sqrt(0.5), 0., np.sqrt(0.5)]))

        # -90 degree rotation around Y axis
        q = quaternion.create_from_y_rotation(-np.pi / 2.)

    def test_create_from_z_rotation(self):
        # 180 degree turn around Z axis
        q = quaternion.create_from_z_rotation(np.pi)
        self.assertTrue(np.allclose(q, [0., 0., 1., 0.]))

        # 90 degree rotation around Z axis
        q = quaternion.create_from_z_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(q, [0., 0., np.sqrt(0.5), np.sqrt(0.5)]))

        # -90 degree rotation around Z axis
        q = quaternion.create_from_z_rotation(-np.pi / 2.)

    def test_create_from_axis_rotation(self):
        # wolfram alpha can be awesome sometimes
        result = quaternion.create_from_axis_rotation([0.57735, 0.57735, 0.57735], np.pi)
        np.testing.assert_almost_equal(result, [5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17], decimal=3)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_axis_rotation_non_normalized(self):
        result = quaternion.create_from_axis_rotation([1., 1., 1.], np.pi)
        np.testing.assert_almost_equal(result, [5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17], decimal=3)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix_unit(self):
        result = quaternion.create_from_matrix(np.eye(3))
        np.testing.assert_almost_equal(result, [0., 0., 0., 1.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix_x(self):
        result = quaternion.create_from_matrix([
            [1., 0., 0.],
            [0., -1., 0.],
            [0., 0., -1.],
        ])
        np.testing.assert_almost_equal(result, [1., 0., 0., 0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix_y(self):
        result = quaternion.create_from_matrix([
            [-1., 0., 0.],
            [0., 1., 0.],
            [0., 0., -1.],
        ])
        np.testing.assert_almost_equal(result, [0., 1., 0., 0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix_z(self):
        result = quaternion.create_from_matrix([
            [-1., 0., 0.],
            [0., -1., 0.],
            [0., 0., 1.],
        ])
        np.testing.assert_almost_equal(result, [0., 0., 1., 0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    @unittest.skip('Not implemented')
    def test_create_from_eulers(self):
        pass

    @unittest.skip('Not implemented')
    def test_create_from_inverse_of_eulers(self):
        pass

    def test_cross(self):
        q1 = quaternion.create_from_x_rotation(np.pi / 2.0)
        q2 = quaternion.create_from_x_rotation(-np.pi / 2.0)
        result = quaternion.cross(q1, q2)
        np.testing.assert_almost_equal(result, quaternion.create(), decimal=5)


    def test_quaternion_slerp(self):
        sqrt2 = np.sqrt(2) / 2

        identity = np.array([0.0, 0.0, 0.0, 1.0])
        y90rot = np.array([0.0, sqrt2, 0.0, sqrt2])
        y180rot = np.array([0.0, 1.0, 0.0, 0.0])

        # Testing a == 0
        # Must be id
        result = quaternion.slerp(identity, y90rot, 0.0)
        np.testing.assert_almost_equal(result, identity, decimal=4)

        # Testing a == 1
        # Must be 90° rotation on Y : 0 0.7 0 0.7
        result = quaternion.slerp(identity, y90rot, 1.0)
        np.testing.assert_almost_equal(result, y90rot, decimal=4)

        # Testing standard, easy case
        # Must be 45° rotation on Y : 0 0.38 0 0.92
        y45rot1 = quaternion.slerp(identity, y90rot, 0.5)

        # Testing reverse case
        # Must be 45° rotation on Y : 0 0.38 0 0.92
        y45rot2 = quaternion.slerp(y90rot, identity, 0.5)
        np.testing.assert_almost_equal(y45rot1, y45rot2, decimal=4)

        # Testing against full circle around the sphere instead of shortest path
        # Must be 45° rotation on Y
        # certainly not a 135° rotation
        # y45rot3 = quaternion.slerp(identity, quaternion.negate(y90rot), 0.5)
        y45rot3 = quaternion.slerp(identity, y90rot, 0.5)
        y45angle3 = quaternion.rotation_angle(y45rot3)
        np.testing.assert_almost_equal(y45angle3 * 180 / np.pi, 45, decimal=4)
        np.testing.assert_almost_equal(y45angle3, np.pi / 4, decimal=4)

        # # Same, but inverted
        # # Must also be 45° rotation on Y :  0 0.38 0 0.92
        # # -0 -0.38 -0 -0.92 is ok too
        y45rot4 = quaternion.slerp(-y90rot, identity, 0.5)
        np.testing.assert_almost_equal(np.abs(y45rot4), y45rot2, decimal=4)

        # # Testing q1 = q2
        # # Must be 90° rotation on Y : 0 0.7 0 0.7
        y90rot3 = quaternion.slerp(y90rot, y90rot, 0.5);
        np.testing.assert_almost_equal(y90rot3, y90rot, decimal=4)

        # # Testing 180° rotation
        # # Must be 90° rotation on almost any axis that is on the XZ plane
        xz90rot = quaternion.slerp(identity, -y90rot, 0.5)
        xz90rot = quaternion.rotation_angle(xz90rot)
        np.testing.assert_almost_equal(xz90rot, np.pi / 4, decimal=4)

    def test_is_zero_length(self):
        result = quaternion.is_zero_length([1., 0., 0., 0.])
        self.assertFalse(result)

    def test_is_zero_length_zero(self):
        result = quaternion.is_zero_length([0., 0., 0., 0.])
        self.assertTrue(result)

    def test_is_non_zero_length(self):
        result = quaternion.is_non_zero_length([1., 0., 0., 0.])
        self.assertTrue(result)

    def test_is_non_zero_length_zero(self):
        result = quaternion.is_non_zero_length([0., 0., 0., 0.])
        self.assertFalse(result)

    def test_squared_length_identity(self):
        result = quaternion.squared_length([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_squared_length(self):
        result = quaternion.squared_length([1., 1., 1., 1.])
        np.testing.assert_almost_equal(result, 4., decimal=5)

    def test_squared_length_batch(self):
        result = quaternion.squared_length([
            [0., 0., 0., 1.],
            [1., 1., 1., 1.],
        ])
        np.testing.assert_almost_equal(result, [1., 4.], decimal=5)

    def test_length_identity(self):
        result = quaternion.length([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, 1., decimal=5)

    def test_length(self):
        result = quaternion.length([1., 1., 1., 1.])
        np.testing.assert_almost_equal(result, 2., decimal=5)

    def test_length_batch(self):
        result = quaternion.length([
            [0., 0., 0., 1.],
            [1., 1., 1., 1.],
        ])
        np.testing.assert_almost_equal(result, [1., 2.], decimal=5)

    def test_normalize_identity(self):
        # normalize an identity quaternion
        result = quaternion.normalize([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, [0., 0., 0., 1.], decimal=5)

    def test_normalize_non_identity(self):
        # normalize an identity quaternion
        result = quaternion.normalize([1., 2., 3., 4.])
        np.testing.assert_almost_equal(result, [1. / np.sqrt(30.), np.sqrt(2. / 15.), np.sqrt(3. / 10.), 2. * np.sqrt(2. / 15.)], decimal=5)

    def test_normalize_batch(self):
        # normalize an identity quaternion
        result = quaternion.normalize([
            [0., 0., 0., 1.],
            [1., 2., 3., 4.],
        ])
        expected = [
            [0., 0., 0., 1.],
            [1. / np.sqrt(30.), np.sqrt(2. / 15.), np.sqrt(3. / 10.), 2. * np.sqrt(2. / 15.)],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_rotation_angle(self):
        result = quaternion.rotation_angle([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17])
        np.testing.assert_almost_equal(result, np.pi, decimal=5)

    def test_rotation_axis(self):
        result = quaternion.rotation_axis([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17])
        np.testing.assert_almost_equal(result, [0.57735, 0.57735, 0.57735], decimal=5)

    def test_dot_adjacent(self):
        result = quaternion.dot([1., 0., 0., 0.], [0., 1., 0., 0.])
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_dot_parallel(self):
        result = quaternion.dot([0., 1., 0., 0.], [0., 1., 0., 0.])
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_dot_angle(self):
        result = quaternion.dot([.2, .2, 0., 0.], [2., -.2, 0., 0.])
        np.testing.assert_almost_equal(result, 0.36, decimal=5)

    def test_dot_batch(self):
        result = quaternion.dot([
            [1., 0., 0., 0.],
            [0., 1., 0., 0.],
            [.2, .2, 0., 0.]
        ], [
            [0., 1., 0., 0.],
            [0., 1., 0., 0.],
            [2., -.2, 0., 0.]
        ])
        expected = [0., 1., 0.36]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_conjugate(self):
        #result = quaternion.conjugate([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17])
        result = quaternion.conjugate([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, [0., 0., 0., 1.], decimal=5)

    def test_conjugate_rotation(self):
        result = quaternion.conjugate([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17])
        np.testing.assert_almost_equal(result, [-0.57735, -0.57735, -0.57735, 6.12323e-17], decimal=5)

    @unittest.skip('Not implemented')
    def test_power(self):
        pass

    def test_inverse(self):
        result = quaternion.inverse([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, [0., 0., 0., 1.], decimal=5)

    def test_inverse_rotation(self):
        result = quaternion.inverse([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17])
        np.testing.assert_almost_equal(result, [-0.577351, -0.577351, -0.577351, 6.12324e-17], decimal=5)

    def test_inverse_non_unit(self):
        q = [1, 2, 3, 4]
        result = quaternion.inverse(q)
        expected = quaternion.conjugate(q) / quaternion.length(q)
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_negate_unit(self):
        result = quaternion.negate([0., 0., 0., 1.])
        np.testing.assert_almost_equal(result, [0., 0., 0., -1.], decimal=5)

    def test_negate(self):
        result = quaternion.negate([1., 2., 3., 4.])
        np.testing.assert_almost_equal(result, [-1., -2., -3., -4.], decimal=5)

    def test_apply_to_vector_unit_x(self):
        result = quaternion.apply_to_vector([0., 0., 0., 1.], [1., 0., 0.])
        np.testing.assert_almost_equal(result, [1., 0., 0.], decimal=5)

    def test_apply_to_vector_x(self):
        # 180 degree turn around X axis
        q = quaternion.create_from_x_rotation(np.pi)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0.,-1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 0.,-1.]))

        # 90 degree rotation around X axis
        q = quaternion.create_from_x_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0., 0., 1.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0.,-1., 0.]))

        # -90 degree rotation around X axis
        q = quaternion.create_from_x_rotation(-np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0., 0.,-1.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 1., 0.]))

    def test_apply_to_vector_y(self):
        # 180 degree turn around Y axis
        q = quaternion.create_from_y_rotation(np.pi)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [-1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0., 1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 0.,-1.]))

        # 90 degree rotation around Y axis
        q = quaternion.create_from_y_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [0., 0.,-1.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0., 1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [1., 0., 0.]))

        # -90 degree rotation around Y axis
        q = quaternion.create_from_y_rotation(-np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [0., 0., 1.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0., 1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [-1., 0., 0.]))

    def test_apply_to_vector_z(self):
        # 180 degree turn around Z axis
        q = quaternion.create_from_z_rotation(np.pi)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [-1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [0.,-1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 0., 1.]))

        # 90 degree rotation around Z axis
        q = quaternion.create_from_z_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [0., 1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [-1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 0., 1.]))

        # -90 degree rotation around Z axis
        q = quaternion.create_from_z_rotation(-np.pi / 2.)
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [1., 0., 0.]), [0.,-1., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 1., 0.]), [1., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 1.]), [0., 0., 1.]))

    def test_apply_to_vector_non_unit(self):
        q = quaternion.create_from_x_rotation(np.pi)
        # zero length
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 0.]), [0., 0., 0.]))

        # >1 length
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [2., 0., 0.]), [2., 0., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 2., 0.]), [0.,-2., 0.]))
        self.assertTrue(np.allclose(quaternion.apply_to_vector(q, [0., 0., 2.]), [0., 0.,-2.]))

    def test_identity(self):
        # https://en.wikipedia.org/wiki/Quaternion
        i = quaternion.create(1., 0., 0., 0.)
        j = quaternion.create(0., 1., 0., 0.)
        k = quaternion.create(0., 0., 1., 0.)
        one = quaternion.create(0., 0., 0., 1.)

        # i * 1 = i
        # j * 1 = j
        # k * 1 = k
        # 1 * i = i
        # 1 * j = j
        # 1 * k = k
        i1 = quaternion.cross(i, one)
        j1 = quaternion.cross(j, one)
        k1 = quaternion.cross(k, one)
        _1i = quaternion.cross(one, i)
        _1j = quaternion.cross(one, j)
        _1k = quaternion.cross(one, k)

        self.assertTrue(np.allclose(i1, _1i, i))
        self.assertTrue(np.allclose(j1, _1j, j))
        self.assertTrue(np.allclose(k1, _1k, k))

        # result = -1
        ii = quaternion.cross(i, i)
        kk = quaternion.cross(k, k)
        jj = quaternion.cross(j, j)
        ijk = quaternion.cross(quaternion.cross(i, j), k)

        self.assertTrue(np.allclose(ii, -one))
        self.assertTrue(np.allclose(jj, -one))
        self.assertTrue(np.allclose(kk, -one))
        self.assertTrue(np.allclose(ijk, -one))

        # ij = k
        # ji = -k
        # jk = i
        # kj = -i
        # ki = j
        # ik = -j

        ij = quaternion.cross(i, j)
        ji = quaternion.cross(j, i)
        jk = quaternion.cross(j, k)
        kj = quaternion.cross(k, j)
        ki = quaternion.cross(k, i)
        ik = quaternion.cross(i, k)

        self.assertTrue(np.allclose(ij, k))
        self.assertTrue(np.allclose(ji, -k))
        self.assertTrue(np.allclose(jk, i))
        self.assertTrue(np.allclose(kj, -i))
        self.assertTrue(np.allclose(ki, j))
        self.assertTrue(np.allclose(ik, -j))

        # -k = ijkk = ij(k^2) = ij(-1)

        ijkk = quaternion.cross(quaternion.cross(ij, k), k)
        ijk2 = quaternion.cross(ij, quaternion.cross(k, k))
        ij_m1 = quaternion.cross(ij, -one)

        self.assertTrue(np.allclose(ijkk, ijk2))
        self.assertTrue(np.allclose(ijk2, ij_m1))


if __name__ == '__main__':
    unittest.main()

try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import matrix33, quaternion, vector3


class test_matrix33(unittest.TestCase):
    # use wolfram alpha to get information on quaternion conversion values
    # be aware that wolfram lists it as w,x,y,z
    def test_import(self):
        import pyrr
        pyrr.matrix33
        from pyrr import matrix33

    def test_create_from_quaternion_unit(self):
        result = matrix33.create_from_quaternion([0.,0.,0.,1.])
        np.testing.assert_almost_equal(result, np.eye(3), decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_quaternion_x(self):
        result = matrix33.create_from_quaternion([1.,0.,0.,0.])
        expected = [
            [1.,0.,0.],
            [0.,-1.,0.],
            [0.,0.,-1.],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_quaternion_y(self):
        result = matrix33.create_from_quaternion([0.,1.,0.,0.])
        expected = [
            [-1.,0.,0.],
            [0.,1.,0.],
            [0.,0.,-1.],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_quaternion_z(self):
        result = matrix33.create_from_quaternion([0.,0.,1.,0.])
        expected = [
            [-1.,0.,0.],
            [0.,-1.,0.],
            [0.,0.,1.],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_quaternion_rotation(self):
        result = matrix33.create_from_quaternion([.57735,.57735,.57735,0.])
        expected = [
            [-0.333333, 0.666667, 0.666667],
            [0.666667, -0.333333, 0.666667],
            [0.666667, 0.666667, -0.333333],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_quaternion_equivalent(self):
        result = matrix33.create_from_quaternion(quaternion.create_from_x_rotation(0.5))
        expected = matrix33.create_from_x_rotation(0.5)
        np.testing.assert_almost_equal(result, expected, decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_inverse_equivalence(self):
        q = [5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17]
        result = matrix33.create_from_quaternion(quaternion.inverse(q))
        expected = matrix33.inverse(matrix33.create_from_quaternion(q))
        np.testing.assert_almost_equal(result, expected, decimal=5)

        q = quaternion.create_from_x_rotation(0.5)
        result = matrix33.create_from_inverse_of_quaternion(q)
        expected = matrix33.inverse(matrix33.create_from_quaternion(q))
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_create_from_inverse_of_quaternion(self):
        q = quaternion.create_from_x_rotation(np.pi / 2.0)
        result = matrix33.create_from_inverse_of_quaternion(q)
        self.assertTrue(np.allclose(result, matrix33.create_from_x_rotation(-np.pi / 2.0)))

    def test_create_identity(self):
        result = matrix33.create_identity()
        np.testing.assert_almost_equal(result, np.eye(3), decimal=5)
        self.assertTrue(result.dtype == np.float)

    def create_from_matrix44(self):
        m44 = np.arange((4,4))
        result = matrix33.create_from_matrix44(m44)
        self.assertTrue(np.allclose(result, m44[:3][:3]))

    @unittest.skip('Not implemented')
    def test_create_from_eulers(self):
        # just call the function
        # TODO: check the result
        matrix33.create_from_eulers([1,2,3])

    def test_create_from_axis_rotation(self):
        # wolfram alpha can be awesome sometimes
        result = matrix33.create_from_axis_rotation([0.57735, 0.57735, 0.57735],np.pi)
        np.testing.assert_almost_equal(result, matrix33.create_from_quaternion([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17]), decimal=3)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_axis_rotation_non_normalized(self):
        result = matrix33.create_from_axis_rotation([1.,1.,1.], np.pi)
        np.testing.assert_almost_equal(result, matrix33.create_from_quaternion([5.77350000e-01, 5.77350000e-01, 5.77350000e-01, 6.12323400e-17]), decimal=3)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_x_rotation(self):
        mat = matrix33.create_from_x_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(np.dot([1.,0.,0.], mat), [1.,0.,0.]))
        self.assertTrue(np.allclose(np.dot([0.,1.,0.], mat), [0.,0.,-1.]))
        self.assertTrue(np.allclose(np.dot([0.,0.,1.], mat), [0.,1.,0.]))

    def test_create_from_y_rotation(self):
        mat = matrix33.create_from_y_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(np.dot([1.,0.,0.], mat), [0.,0.,1.]))
        self.assertTrue(np.allclose(np.dot([0.,1.,0.], mat), [0.,1.,0.]))
        self.assertTrue(np.allclose(np.dot([0.,0.,1.], mat), [-1.,0.,0.]))

    def test_create_from_z_rotation(self):
        mat = matrix33.create_from_z_rotation(np.pi / 2.)
        self.assertTrue(np.allclose(np.dot([1.,0.,0.], mat), [0.,-1.,0.]))
        self.assertTrue(np.allclose(np.dot([0.,1.,0.], mat), [1.,0.,0.]))
        self.assertTrue(np.allclose(np.dot([0.,0.,1.], mat), [0.,0.,1.]))

    def test_create_from_scale(self):
        scale = np.array([ 2.0, 3.0, 4.0])
        mat = matrix33.create_from_scale(scale)
        result = mat.diagonal()
        expected = scale
        self.assertTrue(np.array_equal(result, expected))

    def test_create_from_quaternion_identity(self):
        quat = quaternion.create()
        result = matrix33.create_from_quaternion(quat)
        expected = np.eye(3)
        self.assertTrue(np.array_equal(result, expected))

    def test_create_from_quaternion_rotated_x(self):
        quat = quaternion.create_from_x_rotation(np.pi)
        result = matrix33.create_from_quaternion(quat)
        expected = matrix33.create_from_x_rotation(np.pi)
        self.assertTrue(np.allclose(result, expected))

    def test_create_from_quaternion_rotated_y(self):
        quat = quaternion.create_from_y_rotation(np.pi)
        result = matrix33.create_from_quaternion(quat)
        expected = matrix33.create_from_y_rotation(np.pi)
        self.assertTrue(np.allclose(result, expected))

    def test_create_from_quaternion_rotated_z(self):
        quat = quaternion.create_from_z_rotation(np.pi)
        result = matrix33.create_from_quaternion(quat)
        expected = matrix33.create_from_z_rotation(np.pi)
        self.assertTrue(np.allclose(result, expected))

    def test_apply_to_vector_identity(self):
        mat = matrix33.create_identity()
        vec = vector3.unit.x
        result = matrix33.apply_to_vector(mat, vec)
        expected = vec
        self.assertTrue(np.array_equal(result, expected))

    def test_apply_to_vector_rotated_x(self):
        mat = matrix33.create_from_x_rotation(np.pi)
        vec = vector3.unit.y
        result = matrix33.apply_to_vector(mat, vec)
        expected = -vec
        self.assertTrue(np.allclose(result, expected))

    def test_apply_to_vector_rotated_y(self):
        mat = matrix33.create_from_y_rotation(np.pi)
        vec = vector3.unit.x
        result = matrix33.apply_to_vector(mat, vec)
        expected = -vec
        self.assertTrue(np.allclose(result, expected))

    def test_apply_to_vector_rotated_z(self):
        mat = matrix33.create_from_z_rotation(np.pi)
        vec = vector3.unit.x
        result = matrix33.apply_to_vector(mat, vec)
        expected = -vec
        self.assertTrue(np.allclose(result, expected))

    def test_multiply_identity(self):
        m1 = matrix33.create_identity()
        m2 = matrix33.create_identity()
        result = matrix33.multiply(m1, m2)
        self.assertTrue(np.allclose(result, np.dot(m1,m2)))

    def test_multiply_rotation(self):
        m1 = matrix33.create_from_x_rotation(np.pi)
        m2 = matrix33.create_from_y_rotation(np.pi / 2.0)
        result = matrix33.multiply(m1, m2)
        self.assertTrue(np.allclose(result, np.dot(m1,m2)))

    def test_inverse(self):
        m = matrix33.create_from_y_rotation(np.pi)
        result = matrix33.inverse(m)
        self.assertTrue(np.allclose(result, matrix33.create_from_y_rotation(-np.pi)))

    def test_create_direction_scale(self):
        m = matrix33.create_direction_scale([0.,1.,0.], 0.5)
        v = np.array([
            [1.,0.,0.],
            [1.,1.,1.],
            [10.,10.,10.]
        ])
        result = np.array([
            matrix33.apply_to_vector(m, v[0]),
            matrix33.apply_to_vector(m, v[1]),
            matrix33.apply_to_vector(m, v[2]),
        ])
        expected = np.array([
            [1.,0.,0.],
            [1.,.5,1.],
            [10.,5.,10.]
        ])
        self.assertTrue(np.allclose(result, expected))

if __name__ == '__main__':
    unittest.main()

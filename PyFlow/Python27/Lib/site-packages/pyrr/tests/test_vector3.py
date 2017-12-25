try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import vector3


class test_vector3(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.vector3
        from pyrr import vector3

    def test_create(self):
        result = vector3.create()
        np.testing.assert_almost_equal(result, [0.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_values(self):
        result = vector3.create(1., 2., 3., dtype=np.float32)
        np.testing.assert_almost_equal(result, [1.,2.,3.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_list(self):
        with self.assertRaises(ValueError):
            vector3.create([1., 2., 3.])

    def test_create_unit_length_x(self):
        result = vector3.create_unit_length_x()
        np.testing.assert_almost_equal(result, [1.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_x_dtype(self):
        result = vector3.create_unit_length_x(dtype=np.float32)
        np.testing.assert_almost_equal(result, [1.,0.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_unit_length_y(self):
        result = vector3.create_unit_length_y()
        np.testing.assert_almost_equal(result, [0.,1.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_y_dtype(self):
        result = vector3.create_unit_length_y(dtype=np.float32)
        np.testing.assert_almost_equal(result, [0.,1.,0.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_unit_length_z(self):
        result = vector3.create_unit_length_z()
        np.testing.assert_almost_equal(result, [0.,0.,1.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_unit_length_z_dtype(self):
        result = vector3.create_unit_length_z(dtype=np.float32)
        np.testing.assert_almost_equal(result, [0.,0.,1.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_create_from_vector4(self):
        v4 = [1., 2., 3., 4.]
        result = vector3.create_from_vector4(v4)
        v, w = result
        np.testing.assert_almost_equal(v, [1.,2.,3.], decimal=5)
        np.testing.assert_almost_equal(w, 4., decimal=5)

    def test_create_from_matrix44_translation(self):
        mat = np.array([
            [1.,2.,3.,4.,],
            [5.,6.,7.,8.,],
            [9.,10.,11.,12.,],
            [13.,14.,15.,16.,],
        ])
        result = vector3.create_from_matrix44_translation(mat)
        np.testing.assert_almost_equal(result, [13.,14.,15.], decimal=5)
        self.assertTrue(result.dtype == np.float)

    def test_create_from_matrix44_translation_dtype_matches(self):
        mat = np.array([
            [1.,2.,3.,4.,],
            [5.,6.,7.,8.,],
            [9.,10.,11.,12.,],
            [13.,14.,15.,16.,],
        ], dtype=np.float32)
        result = vector3.create_from_matrix44_translation(mat)
        np.testing.assert_almost_equal(result, [13.,14.,15.], decimal=5)
        self.assertTrue(result.dtype == np.float32)

    def test_normalize_single_vector(self):
        result = vector3.normalize([1.,1.,1.])
        np.testing.assert_almost_equal(result, [0.57735, 0.57735, 0.57735], decimal=5)

    def test_normalize_batch(self):
        result = vector3.normalize([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            [0.57735, 0.57735, 0.57735],
            [-0.57735,-0.57735,-0.57735],
            [0., 0.274721, 0.961524],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_generate_normals(self):
        vertices = np.array([
            [2.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [2.0, 2.0, 0.0]
        ])
        index = np.array([
            [0, 2, 1],
            [0, 3, 2],
        ])
        v1, v2, v3 = np.rollaxis(vertices[index], axis=1)
        result = vector3.generate_normals(v1, v2, v3)
        expected = np.array([
            [0., 0., 1.],
            [0., 0., 1.]
        ])
        np.testing.assert_array_equal(result, expected)

    def test_generate_normals_unnormalized(self):
        vertices = np.array([
            [2.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [2.0, 2.0, 0.0]
        ])
        index = np.array([
            [0, 2, 1],
            [0, 3, 2],
        ])
        v1, v2, v3 = np.rollaxis(vertices[index], axis=1)
        result = vector3.generate_normals(v1, v2, v3, normalize_result=False)
        expected = np.array([
            [0., 0., 4.],
            [0., 0., 4.]
        ])
        np.testing.assert_array_equal(result, expected)

    def test_generate_vertex_normals(self):
        vertices = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0]
        ])
        index = np.array([
            [0, 2, 1],
            [0, 3, 2],
        ])
        result = vector3.generate_vertex_normals(vertices, index)
        expected = np.array([
            [0., 0., 1.],
            [0., 0., 1.],
            [0., 0., 1.],
            [0., 0., 1.]
        ])
        np.testing.assert_array_equal(result, expected)
    
    def test_generate_vertex_normals_unnormalized(self):
        vertices = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0]
        ])
        index = np.array([
            [0, 2, 1],
            [0, 3, 2],
        ])
        result = vector3.generate_vertex_normals(
            vertices, index, normalize_result=False)
        expected = np.array([
            [0., 0., 2.],
            [0., 0., 1.],
            [0., 0., 2.],
            [0., 0., 1.]
        ])
        np.testing.assert_array_equal(result, expected)

    def test_squared_length_single_vector(self):
        result = vector3.squared_length([1.,1.,1.])
        np.testing.assert_almost_equal(result, 3., decimal=5)

    def test_squared_length_batch(self):
        result = vector3.squared_length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            3.,
            3.,
            53.,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_length(self):
        result = vector3.length([1.,1.,1.])
        np.testing.assert_almost_equal(result, 1.73205, decimal=5)

    def test_length_batch(self):
        result = vector3.length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
        ])
        expected = [
            1.73205,
            1.73205,
            7.28011,
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length(self):
        result = vector3.set_length([1.,1.,1.],2.)
        expected = [1.15470,1.15470,1.15470]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_set_length_batch_vector(self):
        result = vector3.set_length([
            [1.,1.,1.],
            [-1.,-1.,-1.],
            [0.,2.,7.],
            ], 2.0)
        expected = [
            [1.15470,1.15470,1.15470],
            [-1.15470,-1.15470,-1.15470],
            [0.,0.54944,1.92304],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_dot_adjacent(self):
        result = vector3.dot([1.,0.,0.], [0.,1.,0.])
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_dot_parallel(self):
        result = vector3.dot([0.,1.,0.], [0.,1.,0.])
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_dot_angle(self):
        result = vector3.dot([.2,.2,0.], [2.,-.2,0.])
        np.testing.assert_almost_equal(result, 0.36, decimal=5)

    def test_dot_batch(self):
        result = vector3.dot([
            [1.,0.,0.],
            [0.,1.,0.],
            [.2,.2,0.]
        ],[
            [0.,1.,0.],
            [0.,1.,0.],
            [2.,-.2,0.]
        ])
        expected = [
            0.,
            1.,
            0.36
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_cross_single_vector(self):
        result = vector3.cross([1.,0.,0.], [0.,1.,0.])
        np.testing.assert_almost_equal(result, [0.,0.,1.], decimal=5)

    def test_cross_coincident(self):
        result = vector3.cross([1.,0.,0.], [1.,0.,0.])
        np.testing.assert_almost_equal(result, [0.,0.,0.], decimal=5)

    def test_cross_batch(self):
        result = vector3.cross([
            [1.,0.,0.],
            [0.,0.,1.]
        ],[
            [0.,1.,0.],
            [0.,1.,0.],
        ])
        expected = [
            [0.,0.,1.],
            [-1.,0.,0.],
        ]
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_interoplation( self ):
        result = vector3.interpolate([0.,0.,0.], [1.,1.,1.], 0.5)
        np.testing.assert_almost_equal(result, [.5,.5,.5], decimal=5)

        result = vector3.interpolate([0.,0.,0.], [2.,2.,2.], 0.5)
        np.testing.assert_almost_equal(result, [1.,1.,1.], decimal=5)


if __name__ == '__main__':
    unittest.main()

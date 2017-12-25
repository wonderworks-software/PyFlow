try:
    import unittest2 as unittest
except:
    import unittest
import numpy as np
from pyrr import geometric_tests as gt
from pyrr import line, plane, ray, sphere

class test_geometric_tests(unittest.TestCase):
    def test_import(self):
        import pyrr
        pyrr.geometric_tests
        from pyrr import geometric_tests

    def test_point_intersect_line(self):
        p = np.array([1.,1.,1.])
        l = np.array([[0.,0.,0.],[2.,2.,2.]])
        result = gt.point_intersect_line(p, l)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_line_invalid(self):
        p = np.array([3.,3.,3.])
        l = np.array([[0.,0.,0.],[2.,2.,2.]])
        result = gt.point_intersect_line(p, l)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_line_segment(self):
        p = np.array([1.,1.,1.])
        l = np.array([[0.,0.,0.],[2.,2.,2.]])
        result = gt.point_intersect_line_segment(p, l)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_line_segment_invalid(self):
        p = np.array([3.,3.,3.])
        l = np.array([[0.,0.,0.],[2.,2.,2.]])
        result = gt.point_intersect_line_segment(p, l)
        self.assertEqual(result, None)

    def test_point_intersect_rectangle_valid_intersections_1(self):
        r = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])
        p = [ 0.0, 0.0]
        result = gt.point_intersect_rectangle(p, r)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_rectangle_valid_intersections_2(self):
        r = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])
        p = [ 5.0, 5.0]
        result = gt.point_intersect_rectangle(p, r)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_rectangle_valid_intersections_3(self):
        r = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])
        p = [ 1.0, 1.0]
        result = gt.point_intersect_rectangle(p, r)
        self.assertTrue(np.array_equal(result, p))

    def test_point_intersect_rectangle_invalid_intersections_1(self):
        r = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])

        p = [-1.0, 1.0]
        result = gt.point_intersect_rectangle(p, r)
        self.assertFalse(np.array_equal(result, p))

    def test_point_intersect_rectangle_invalid_intersections_2(self):
        r = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])
        p = [ 1.0, 10.0]
        result = gt.point_intersect_rectangle(p, r)
        self.assertFalse(np.array_equal(result, p))

    def test_point_intersect_rectangle_invalid_intersections_3(self):
        rect = np.array([
            [0.0, 0.0],
            [5.0, 5.0]
        ])
        point = [ 1.0,-1.0]
        result = gt.point_intersect_rectangle(point, rect)
        self.assertFalse(np.array_equal(result, point))

    def test_ray_intersect_plane(self):
        r = ray.create([0.,-1.,0.],[0.,1.,0.])
        p = plane.create([0.,1.,0.], 0.)
        result = gt.ray_intersect_plane(r, p)
        self.assertFalse(np.array_equal(result, [0.,1.,0.]))

    def test_ray_intersect_plane_front_only(self):
        r = ray.create([0.,-1.,0.],[0.,1.,0.])
        p = plane.create([0.,1.,0.], 0.)
        result = gt.ray_intersect_plane(r, p, front_only=True)
        self.assertEqual(result, None)

    def test_ray_intersect_plane_invalid(self):
        r = ray.create([0.,-1.,0.],[1.,0.,0.])
        p = plane.create([0.,1.,0.], 0.)
        result = gt.ray_intersect_plane(r, p)
        self.assertEqual(result, None)

    def test_point_closest_point_on_ray(self):
        l = line.create_from_points(
            [ 0.0, 0.0, 0.0 ],
            [10.0, 0.0, 0.0 ]
        )
        p = np.array([ 0.0, 1.0, 0.0])
        result = gt.point_closest_point_on_ray(p, l)
        self.assertTrue(np.array_equal(result, [ 0.0, 0.0, 0.0]))

    def test_point_closest_point_on_line(self):
        p = np.array([0.,1.,0.])
        l = np.array([[0.,0.,0.],[2.,0.,0.]])
        result = gt.point_closest_point_on_line(p, l)
        self.assertTrue(np.array_equal(result, [0.,0.,0.]), (result,))

    def test_point_closest_point_on_line_2(self):
        p = np.array([3.,0.,0.])
        l = np.array([[0.,0.,0.],[2.,0.,0.]])
        result = gt.point_closest_point_on_line(p, l)
        self.assertTrue(np.array_equal(result, [3.,0.,0.]), (result,))

    def test_point_closest_point_on_line_segment(self):
        p = np.array([0.,1.,0.])
        l = np.array([[0.,0.,0.],[2.,0.,0.]])
        result = gt.point_closest_point_on_line_segment(p, l)
        self.assertTrue(np.array_equal(result, [0.,0.,0.]), (result,))

    def test_vector_parallel_vector(self):
        v1 = np.array([1.,0.,0.])
        v2 = np.array([2.,0.,0.])
        self.assertTrue(gt.vector_parallel_vector(v1,v2))

    def test_vector_parallel_vector_invalid(self):
        v1 = np.array([1.,0.,0.])
        v2 = np.array([0.,1.,0.])
        self.assertTrue(False == gt.vector_parallel_vector(v1,v2))

    def test_ray_parallel_ray(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([1.,0.,0.],[2.,0.,0.])
        self.assertTrue(gt.ray_parallel_ray(r1,r2))

    def test_ray_parallel_ray_2(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([1.,0.,0.],[0.,1.,0.])
        self.assertTrue(False == gt.ray_parallel_ray(r1,r2))

    def test_ray_parallel_ray_3(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([0.,1.,0.],[1.,0.,0.])
        self.assertTrue(gt.ray_parallel_ray(r1,r2))

    def test_ray_coincident_ray(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([1.,0.,0.],[2.,0.,0.])
        self.assertTrue(gt.ray_coincident_ray(r1,r2))

    def test_ray_coincident_ray_2(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([1.,0.,0.],[0.,1.,0.])
        self.assertTrue(False == gt.ray_coincident_ray(r1,r2))

    def test_ray_coincident_ray_3(self):
        r1 = ray.create([0.,0.,0.],[1.,0.,0.])
        r2 = ray.create([0.,1.,0.],[1.,0.,0.])
        self.assertTrue(False == gt.ray_coincident_ray(r1,r2))

    def test_ray_intersect_aabb_valid_1(self):
        a = np.array([[-1.0,-1.0,-1.0], [ 1.0, 1.0, 1.0]])
        r = np.array([[ 0.5, 0.5, 0.0], [ 0.0, 0.0,-1.0]])
        result = gt.ray_intersect_aabb(r, a)
        self.assertTrue(np.array_equal(result, [ 0.5, 0.5,-1.0]))

    def test_ray_intersect_aabb_valid_2(self):
        a = np.array([[-1.0,-1.0,-1.0], [ 1.0, 1.0, 1.0]])
        r = np.array([[2.0, 2.0, 2.0], [ -1.0, -1.0, -1.0]])
        result = gt.ray_intersect_aabb(r, a)
        self.assertTrue(np.array_equal(result, [1.0, 1.0, 1.0]))

    def test_ray_intersect_aabb_invalid_1(self):
        a = np.array([[-1.0,-1.0,-1.0], [ 1.0, 1.0, 1.0]])
        r = np.array([[2.0, 2.0, 2.0], [ 1.0, 1.0, 1.0]])
        result = gt.ray_intersect_aabb(r, a)
        self.assertEqual(result, None)

    def test_point_height_above_plane(self):
        v1 = np.array([ 0.0, 0.0, 1.0])
        v2 = np.array([ 1.0, 0.0, 1.0])
        v3 = np.array([ 0.0, 1.0, 1.0])
        p = np.array([0.0, 0.0, 20.0])

        pl = plane.create_from_points(v1, v2, v3)
        pl = plane.invert_normal(pl)

        result = gt.point_height_above_plane(p, pl)
        self.assertEqual(result, 19.)

    def test_point_closest_point_on_plane(self):
        pl = np.array([ 0.0, 1.0, 0.0, 0.0])
        p = np.array([ 5.0, 20.0, 5.0])
        result = gt.point_closest_point_on_plane(p, pl)
        self.assertTrue(np.array_equal(result, [ 5.0, 0.0, 5.0]))

    def test_sphere_does_intersect_sphere_1(self):
        s1 = sphere.create()
        s2 = sphere.create()
        self.assertTrue(gt.sphere_does_intersect_sphere(s1, s2))

    def test_sphere_does_intersect_sphere_2(self):
        s1 = sphere.create()
        s2 = sphere.create([1.,0.,0.])
        self.assertTrue(gt.sphere_does_intersect_sphere(s1, s2))

    def test_sphere_does_intersect_sphere_3(self):
        s1 = sphere.create()
        s2 = sphere.create([2.,0.,0.], 1.0)
        self.assertTrue(gt.sphere_does_intersect_sphere(s1, s2))

    def test_sphere_does_intersect_sphere_4(self):
        s1 = sphere.create()
        s2 = sphere.create([2.,0.,0.], 0.5)
        self.assertTrue(False == gt.sphere_does_intersect_sphere(s1, s2))

    def test_sphere_penetration_sphere_1(self):
        s1 = sphere.create()
        s2 = sphere.create()
        self.assertEqual(gt.sphere_penetration_sphere(s1, s2), 2.0)

    def test_sphere_penetration_sphere_2(self):
        s1 = sphere.create()
        s2 = sphere.create([1.,0.,0.], 1.0)
        self.assertEqual(gt.sphere_penetration_sphere(s1, s2), 1.0)

    def test_sphere_penetration_sphere_3(self):
        s1 = sphere.create()
        s2 = sphere.create([2.,0.,0.], 1.0)
        self.assertEqual(gt.sphere_penetration_sphere(s1, s2), 0.0)

    def test_sphere_penetration_sphere_4(self):
        s1 = sphere.create()
        s2 = sphere.create([3.,0.,0.], 1.0)
        self.assertEqual(gt.sphere_penetration_sphere(s1, s2), 0.0)

if __name__ == '__main__':
    unittest.main()


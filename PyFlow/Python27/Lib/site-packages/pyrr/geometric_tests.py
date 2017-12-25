# -*- coding: utf-8 -*-
"""Defines a number of functions to test interactions between
various forms data types.
"""
from __future__ import absolute_import, division, print_function
import math
import numpy as np
from . import rectangle, vector, vector3
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays

"""
TODO: line_intersect_plane
TODO: line_segment_intersect_plane
TODO: ray_intersect_ray
TODO: line_intersect_line
TODO: line_segment_intersect_line_segment
"""

@all_parameters_as_numpy_arrays
def point_intersect_line(point, line):
    """Calculates the intersection point of a point and aline.

    Performed by checking if the cross-product
    of the point relative to the line is
    0.
    """
    rl = line[1] - line[0]
    rp = point - line[0]
    cross = vector3.cross(rl, rp)

    # check if the cross product is zero
    if np.count_nonzero(cross) > 0:
        return None
    return point

@all_parameters_as_numpy_arrays
def point_intersect_line_segment(point, line):
    """Calculates the intersection point of a point and a line segment.

    Performed by checking if the cross-product
    of the point relative to the line is
    0 and if the dot product of the point
    relative to the line start AND the end
    point relative to the line start is
    less than the segment's squared length.
    """
    rl = line[1] - line[0]
    rp = point - line[0]
    cross = vector3.cross(rl, rp)
    dot = vector.dot(rp, rl)
    squared_length = vector.squared_length(rl)

    if np.count_nonzero(cross) > 0:
        return None

    if dot < 0.0 or dot > squared_length:
        return None
    return point

@all_parameters_as_numpy_arrays
def point_intersect_rectangle(point, rect):
    """Calculates the intersection point of a point and a 2D rectangle.

    For 3D points, the Z axis will be ignored.

    :return: Returns True if the point is touching
    or within the rectangle.
    """
    left, right, bottom, top = rectangle.bounds(rect)
    if \
        point[0] < left or \
        point[0] > right or \
        point[1] < bottom or \
        point[1] > top:
        return None
    return point

@parameters_as_numpy_arrays('ray', 'plane')
def ray_intersect_plane(ray, plane, front_only=False):
    """Calculates the intersection point of a ray and a plane.

    :param numpy.array ray: The ray to test for intersection.
    :param numpy.array plane: The ray to test for intersection.
    :param boolean front_only: Specifies if the ray should
    only hit the front of the plane.
    Collisions from the rear of the plane will be
    ignored.

    :return The intersection point, or None
    if the ray is parallel to the plane.
    Returns None if the ray intersects the back
    of the plane and front_only is True.
    """
    """
    Distance to plane is defined as
    t = (pd - p0.n) / rd.n
    where:
    rd is the ray direction
    pd is the point on plane . plane normal
    p0 is the ray position
    n is the plane normal

    if rd.n == 0, the ray is parallel to the
    plane.
    """
    p = plane[:3] * plane[3]
    n = plane[:3]
    rd_n = vector.dot(ray[1], n)

    if rd_n == 0.0:
        return None

    if front_only == True:
        if rd_n >= 0.0:
            return None

    pd = vector.dot(p, n)
    p0_n = vector.dot(ray[0], n)
    t = (pd - p0_n) / rd_n
    return ray[0] + (ray[1] * t)

@all_parameters_as_numpy_arrays
def point_closest_point_on_ray(point, ray):
    """Calculates the point on a ray that is closest to a point.

    :param numpy.array point: The point to check with.
    :param numpy.array ray: The ray to check against.
    :rtype: numpy.array
    :return: The closest point on the ray to the point.
    """
    """
    t = (p - rp).n
    cp = rp + (n * t)
    where
    p is the point
    rp is the ray origin
    n is the ray normal of unit length
    t is the distance along the ray to the point
    """
    normalized_n = vector.normalize(ray[1])
    relative_point = (point - ray[0])
    t = vector.dot(relative_point, normalized_n)
    return ray[0] + (normalized_n * t)

@all_parameters_as_numpy_arrays
def point_closest_point_on_line(point, line):
    """Calculates the point on the line that is closest to
    the specified point.

    :param numpy.array point: The point to check with.
    :param numpy.array line: The line to check against.
    :rtype: numpy.array
    :return: The closest point on the line to the point.
    """
    """
    rl = va->b (relative line)
    rp = va->p (relative point)
    u' = u / |u| (normalize)
    cp = a + (u' * (u'.v))
    where:
    a = line start
    b = line end
    p = point
    cp = closest point
    """
    rl = line[1] - line[0]
    rp = point - line[0]
    rl = vector.normalize(rl)
    dot = vector.dot(rl, rp)
    return line[0] + (rl * dot)

@all_parameters_as_numpy_arrays
def point_closest_point_on_line_segment(point, segment):
    """Calculates the point on the line segment that is closest
    to the specified point.

    This is similar to point_closest_point_on_line, except this
    is against the line segment of finite length. Whereas point_closest_point_on_line
    checks against a line of infinite length.

    :param numpy.array point: The point to check with.
    :param numpy.array line_segment: The finite line segment to check against.
    :rtype: numpy.array
    :return: The closest point on the line segment to the point.
    """
    # check if the line has any length
    rl = segment[1] - segment[0]
    squared_length = vector.squared_length(rl)
    if squared_length == 0.0:
        return segment[0]

    rp = point - segment[0]
    # check that / squared_length is correct
    dot = vector.dot(rp, rl) / squared_length;

    if dot < 0.0:
        return segment[0]
    elif dot > 1.0:
        return segment[1]

    # within segment
    # perform the same calculation as closest_point_on_line
    return segment[0] + (rl * dot)

@all_parameters_as_numpy_arrays
def vector_parallel_vector(v1, v2):
    """Checks if two vectors are parallel.

    :param numpy.array v1, v2: The vectors to check.
    :rtype: boolean
    :return: Returns True if the two vectors are parallel.
    """
    # we cross product the 2 vectors
    # if the result is 0, then they are parallel
    cross = vector3.cross(v1, v2)
    return 0 == np.count_nonzero(cross)

@all_parameters_as_numpy_arrays
def ray_parallel_ray(ray1, ray2):
    """Checks if two rays are parallel.

    :param numpy.array ray1, ray2: The rays to check.
    :rtype: boolean
    :return: Returns True if the two rays are parallel.
    """
    # we use a cross product in-case the ray direction
    # isn't unit length
    return vector_parallel_vector(ray1[ 1 ], ray2[ 1 ])

@all_parameters_as_numpy_arrays
def ray_coincident_ray(ray1, ray2):
    """Check if rays are coincident.

    Rays must not only be parallel to each other, but reside
    along the same vector.

    :param numpy.array ray1, ray2: The rays to check.
    :rtype: boolean
    :return: Returns True if the two rays are co-incident.
    """
    # ensure the ray's directions are the same
    if ray_parallel_ray(ray1, ray2):
        # get the delta between the two ray's start point
        delta = ray2[0] - ray1[0]

        # get the cross product of the ray delta and
        # the direction of the rays
        cross = vector3.cross(delta, ray2[1])

        # if the cross product is zero, the start of the
        # second ray is in line with the direction of the
        # first ray
        if np.count_nonzero(cross) > 0:
            return False

        return True
    return False

@all_parameters_as_numpy_arrays
def ray_intersect_aabb(ray, aabb):
    """Calculates the intersection point of a ray and an AABB

    :param numpy.array ray1: The ray to check.
    :param numpy.array aabb: The Axis-Aligned Bounding Box to check against.
    :rtype: numpy.array
    :return: Returns a vector if an intersection occurs.
        Returns None if no intersection occurs.
    """
    """
    http://gamedev.stackexchange.com/questions/18436/most-efficient-aabb-vs-ray-collision-algorithms
    """
    # this is basically "numpy.divide( 1.0, ray[ 1 ] )"
    # except we're trying to avoid a divide by zero warning
    # so where the ray direction value is 0.0, just use infinity
    # which is what we want anyway
    direction = ray[1]
    dir_fraction = np.empty(3, dtype = ray.dtype)
    dir_fraction[direction == 0.0] = np.inf
    dir_fraction[direction != 0.0] = np.divide(1.0, direction[direction != 0.0])

    t1 = (aabb[0,0] - ray[0,0]) * dir_fraction[ 0 ]
    t2 = (aabb[1,0] - ray[0,0]) * dir_fraction[ 0 ]
    t3 = (aabb[0,1] - ray[0,1]) * dir_fraction[ 1 ]
    t4 = (aabb[1,1] - ray[0,1]) * dir_fraction[ 1 ]
    t5 = (aabb[0,2] - ray[0,2]) * dir_fraction[ 2 ]
    t6 = (aabb[1,2] - ray[0,2]) * dir_fraction[ 2 ]


    tmin = max(min(t1, t2), min(t3, t4), min(t5, t6))
    tmax = min(max(t1, t2), max(t3, t4), max(t5, t6))

    # if tmax < 0, ray (line) is intersecting AABB
    # but the whole AABB is behind the ray start
    if tmax < 0:
        return None

    # if tmin > tmax, ray doesn't intersect AABB
    if tmin > tmax:
        return None

    # t is the distance from the ray point
    # to intersection

    t = abs(tmin)
    point = ray[0] + (ray[1] * t)
    return point

@all_parameters_as_numpy_arrays
def point_height_above_plane(point, plane):
    """Calculates how high a point is above a plane.

    :param numpy.array point: The point to check.
    :param numpy.array plane: The plane to check.
    :rtype: float
    :return: The height above the plane as a float. The value will be
        negative if the point is behind the plane.
    """
    """
    http://www.vitutor.com/geometry/distance/point_plane.html
    d(P) = (AX + BY + CZ + D) / sqrt(A^2 + B^2 + C^2)

    Normal is unit length, so it's length is 1.0.
    Therefore, we can ignore the division all together.
    Just perform Pn . [XYZ1]
    """
    return np.dot(plane, [point[0], point[1], point[2], 1.0])

@all_parameters_as_numpy_arrays
def point_closest_point_on_plane(point, plane):
    """Calculates the point on a plane that is closest to a point.

    :param numpy.array point: The point to check with.
    :param numpy.array plane: The infinite plane to check against.
    :rtype: numpy.array
    :return: The closest point on the plane to the point.
    """
    """
    point on plane is defined as:
    q' = q + (d - q.n)n
    where:
    q' is the point on the plane
    q is the point we are checking
    d is the value of normal dot position
    n is the plane normal
    """
    n = plane[:3]
    p = n * plane[3]
    d = np.dot(p, n)
    qn = np.dot(point, n)
    return point + (n * (d - qn))

@all_parameters_as_numpy_arrays
def sphere_does_intersect_sphere(s1, s2):
    """Checks if two spheres overlap.

    Note: This will return True if the two spheres are
    touching perfectly but sphere_penetration_sphere
    will return 0.0 as the touch but don't penetrate.

    This is faster than circle_penetrate_amount_circle
    as it avoids a square root calculation.

    :param numpy.array s1: The first circle.
    :param numpy.array s2: The second circle.
    :rtype: boolean
    :return: Returns True if the circles overlap.
        Otherwise, returns False.
    """
    delta = s2[:3] - s1[:3]
    distance_squared = vector.squared_length(delta)

    radii_squared = math.pow(s1[3] + s2[3], 2.0)

    if distance_squared > radii_squared:
        return False
    return True

@all_parameters_as_numpy_arrays
def sphere_penetration_sphere(s1, s2):
    """Calculates the distance two spheres have penetrated
    into one another.

    :param numpy.array s1: The first circle.
    :param numpy.array s2: The second circle.
    :rtype: float
    :return: The total overlap of the two spheres.
        This is essentially:
        r1 + r2 - distance
        Where r1 and r2 are the radii of circle 1 and 2
        and distance is the length of the vector p2 - p1.
        Will return 0.0 if the circles do not overlap.
    """
    delta = s2[:3] - s1[:3]
    distance = vector.length(delta)

    combined_radii = s1[3] + s2[3]
    penetration = combined_radii - distance

    if penetration <= 0.0:
        return 0.0
    return penetration

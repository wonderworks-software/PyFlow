# -*- coding: utf-8 -*-
"""Provides functions to calculate and manipulate
Axis-Aligned Minimum Bounding Boxes (AAMBB).

AAMBB are a simple 3D rectangle with no orientation.
It is up to the user to provide translation.
AAMBB differ from AABB in that they allow for the
content to rotate freely and still be within the AAMBB.

An AAMBB is represented in the same way an AABB is;
a array of 2 x 3D vectors.
The first vector represents the minimum extent.
The second vector represents the maximum extent.

Note that because the AAMBB set's it's dimensions using
the vector length of any points set within it, the user
should be careful to avoid adding the AAMBB to itself
or the AAMBB will continue to grow.

TODO: add transform( matrix )
TODO: add point_within_aabb
TODO: use point_within_aabb for unit tests
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import aabb, vector
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the minimum vector within the AAMBB
    minimum = 0

    #: The index of the minimum vector within the AAMBB
    maximum = 1


def create_zeros(dtype=None):
    return np.zeros((2,3), dtype=dtype)

@parameters_as_numpy_arrays('min', 'max')
def create_from_bounds(min, max, dtype=None):
    """Creates an AAMBB using the specified minimum
    and maximum values.
    """
    dtype = dtype or min.dtype
    # stack our bounds together and add them as points
    points = np.vstack((min, max))
    return create_from_points(points, dtype)

@parameters_as_numpy_arrays('points')
def create_from_points(points, dtype=None):
    """Creates an AAMBB from the list of specified points.

    Points must be a 2D list. Ie::
        numpy.array([
            [ x, y, z ],
            [ x, y, z ],
            ])
    """
    dtype = dtype or points.dtype

    # convert any negative values to positive
    abs_points = np.absolute(points)

    # find the length of this vector
    length = np.amax(vector.length(abs_points))

    # our AAMBB extends from +length to -length
    # in all directions
    return np.array(
        [
            [-length,-length,-length ],
            [ length, length, length ]
        ],
        dtype=dtype
    )

def create_from_aabbs(aabbs, dtype=None):
    """Creates an AAMBB from a list of existing AABBs.

    AABBs must be a 2D list. Ie::
        numpy.array([
            AABB,
            AABB,
            ])
    """

    aabbs = np.asarray(aabbs)

    dtype = dtype or aabbs.dtype
    # reshape the AABBs as a series of points
    points = aabbs.reshape((-1, 3))

    return create_from_points(points, dtype=dtype)

@parameters_as_numpy_arrays('bb')
def add_points(bb, points):
    """Extends an AAMBB to encompass a list
    of points.

    It should be noted that this ensures that
    the encompassed points can rotate freely.
    Calling this using the min / max points from
    the AAMBB will create an even bigger AAMBB.
    """
    # add our AABB to the list of points
    values = np.vstack((points, bb[0], bb[1]))

    # convert any negative values to positive
    abs_points = np.absolute(values)

    # extract the maximum extent as a vector
    #vec = np.amax(abs_points, axis=0)

    # find the length of this vector
    #length = vector.length(vec)
    length = np.amax(vector.length(abs_points))

    # our AAMBB extends from +length to -length
    # in all directions
    return np.array(
        [
            [-length,-length,-length ],
            [ length, length, length ]
        ],
        dtype=bb.dtype
    )

@parameters_as_numpy_arrays('bbs')
def add_aabbs(bb, bbs):
    """Extend an AAMBB to encompass a list
    of other AABBs or AAMBBs.

    It should be noted that this ensures that
    the encompassed AABBs can rotate freely.
    Using the AAMBB itself in this calculation
    will create an event bigger AAMBB.
    """
    # reshape the AABBs as a series of points
    points = bbs.reshape((-1, 3))

    # use the add_points
    return add_points(bb, points)

def centre_point(bb):
    """Returns the centre point of the AABB.
    This should always be [0.0, 0.0, 0.0]
    """
    return aabb.centre_point(bb)

def minimum(bb):
    """Returns the minimum point of the AABB.
    """
    return aabb.minimum(bb)

def maximum(bb):
    """Returns the maximum point of the AABB.
    """
    return aabb.maximum(bb)

def clamp_points(bb, points):
    """Takes a list of points and modifies them to
    fit within the AABB.
    """
    # use the same function as present in AABB
    aabb.clamp_points(bb, points)


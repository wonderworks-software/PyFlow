# -*- coding: utf-8 -*-
"""Provides functions to calculate and manipulate
Axis-Aligned Bounding Boxes (AABB).

AABB are a simple 3D rectangle with no orientation.
It is up to the user to provide translation.

An AABB is represented by an array of 2 x 3D vectors.
The first vector represents the minimum extent.
The second vector represents the maximum extent.

It should be noted that rotating the object within
an AABB will invalidate the AABB.
It is up to the user to either:

    * recalculate the AABB.
    * use an AAMBB instead.

TODO: add transform( matrix )
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the minimum vector within the AABB
    minimum = 0

    #: The index of the maximum vector within the AABB
    maximum = 1


def create_zeros(dtype=None):
    return np.zeros((2,3), dtype=dtype)

@parameters_as_numpy_arrays('min', 'max')
def create_from_bounds(min, max, dtype=None):
    """Creates an AABB using the specified minimum
    and maximum values.
    """
    dtype = dtype or min.dtype
    return np.array([min, max], dtype=dtype)

@parameters_as_numpy_arrays('points')
def create_from_points(points, dtype=None):
    """Creates an AABB from the list of specified points.

    Points must be a 2D list. Ie::
        numpy.array([
            [ x, y, z ],
            [ x, y, z ],
            ])
    """
    dtype = dtype or points.dtype
    return np.array(
        [
            np.amin(points, axis=0),
            np.amax(points, axis=0)
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('aabbs')
def create_from_aabbs(aabbs, dtype=None):
    """Creates an AABB from a list of existing AABBs.

    AABBs must be a 2D list. Ie::
        numpy.array([
            AABB,
            AABB,
            ])
    """
    dtype = dtype or aabbs.dtype
    # reshape the AABBs as a series of points
    points = aabbs.reshape((-1, 3))

    return create_from_points(points, dtype)

@parameters_as_numpy_arrays('aabb')
def add_points(aabb, points):
    """Extends an AABB to encompass a list
    of points.
    """
    # find the minimum and maximum point values
    minimum = np.amin(points, axis=0)
    maximum = np.amax(points, axis=0)

    # compare to existing AABB
    return np.array(
        [
            np.minimum(aabb[0], minimum),
            np.maximum(aabb[1], maximum)
        ],
        dtype=aabb.dtype
    )

@parameters_as_numpy_arrays( 'aabbs' )
def add_aabbs(aabb, aabbs):
    """Extend an AABB to encompass a list
    of other AABBs.
    """
    # convert to points and use our existing add_points
    # function
    points = aabbs.reshape((-1, 3))

    return add_points(aabb, points)

@all_parameters_as_numpy_arrays
def centre_point(aabb):
    """Returns the centre point of the AABB.
    """
    return (aabb[0] + aabb[1]) * 0.5

@all_parameters_as_numpy_arrays
def minimum(aabb):
    """Returns the minimum point of the AABB.
    """
    return aabb[0].copy()

@all_parameters_as_numpy_arrays
def maximum(aabb):
    """ Returns the maximum point of the AABB.
    """
    return aabb[1].copy()

@all_parameters_as_numpy_arrays
def clamp_points(aabb, points):
    """Takes a list of points and modifies them to
    fit within the AABB.
    """
    return np.clip(points, a_min=aabb[0], a_max=aabb[1])


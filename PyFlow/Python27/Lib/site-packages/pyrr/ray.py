# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Rays.

A ray begins as a single point and extends
infinitely in a direction.

The first vector is the origin of the ray.
The second vector is the direction of the ray
relative to the origin.

The following functions will normalize the ray
direction to unit length.
Some functions may work correctly with directions
that are not unit length, but this may vary from
function to function.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import vector
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the start vector within the ray
    position = 0

    #: The index of the direction vector within the ray
    direction = 1


@parameters_as_numpy_arrays('start', 'direction')
def create(start, direction, dtype=None):
    dtype = dtype or start.dtype
    return np.array(
        [
            start,
            vector.normalize(direction)
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('line')
def create_from_line(line, dtype=None):
    """Converts a line or line segment to a ray.
    """
    dtype = dtype or line.dtype
    # direction = vend - vstart
    return np.array(
        [
            line[0],
            vector.normalize(line[1] - line[0])
        ],
        dtype=dtype
    )

@all_parameters_as_numpy_arrays
def invert(r):
    r2 = r.copy()
    r2[1] *= -1
    return r2

@all_parameters_as_numpy_arrays
def position(ray):
    return ray[0].copy()

@all_parameters_as_numpy_arrays
def direction(ray):
    return ray[1].copy()


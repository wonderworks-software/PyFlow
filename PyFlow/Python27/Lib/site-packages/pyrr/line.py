# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Lines.

A Line data structure is simply a numpy.array with 2 vectors::

    start = numpy.array( [ -1.0, 0.0, 0.0 ] )
    end = numpy.array( [ 1.0, 0.0, 0.0 ] )
    line = numpy.array( [ start, end ] )

Both Lines and Line Segments are defined using the same data structure.
The only difference is how the data is interpreted.

A line is defined by two points but extends infinitely.

A line segment only exists between two points.
It does not extend forever.

The choice to interprete a line as a line or line segment is up to the
function being called. Check the function signature of documentation
to determine how a line will be interpreted.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the start vector within the line
    start = 0

    #: The index of the end vector within the line
    end = 1


def create_zeros(dtype=None):
    """Creates a line with the start and end at the origin.

    :rtype: numpy.array
    :return: A line with both start and end points at (0,0,0).
    """
    return np.zeros((2,3), dtype=dtype)

def create_from_points(v1, v2, dtype=None):
    """Creates a line from 2 vectors.

    The 2 vectors represent the start and end point of the line.

    :param numpy.array v1: Start point.
    :param numpy.array v2: End point.
    :rtype: numpy.array
    :return: A line extending from v1 to v2.
    """
    return np.array([v1, v2], dtype=dtype)

@all_parameters_as_numpy_arrays
def create_from_ray(ray):
    """Converts a ray to a line.

    The line will extend from 'ray origin -> ray origin + ray direction'.

    :param numpy.array ray: The ray to convert.
    :rtype: numpy.array
    :return: A line beginning at the ray start and extending for 1 unit
        in the direction of the ray.
    """
    # convert ray relative direction to absolute
    # position
    return np.array([ray[0], ray[0] + ray[1]], dtype=ray.dtype)

@all_parameters_as_numpy_arrays
def start(line):
    """Extracts the start point of the line.

    :param numpy.array line: The line to extract the start from.
    :rtype: numpy.array
    :return: The starting point of the line.
    """
    return line[0].copy()

@all_parameters_as_numpy_arrays
def end(line):
    """Extracts the end point of the line.

    :param numpy.array line: The line to extract the end from.
    :rtype: numpy.array
    :return: The ending point of the line.
    """
    return line[1].copy()


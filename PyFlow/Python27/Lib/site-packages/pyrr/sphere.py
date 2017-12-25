# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of 3D Spheres.

Sphere are represented using a numpy.array of shape (4,).

The first three values are the sphere's position.
The fourth value is the sphere's radius.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays

@parameters_as_numpy_arrays('center')
def create(center=None, radius=1.0, dtype=None):
    if center is None:
        center = [0.,0.,0.]
    return np.array([center[0], center[1], center[2], radius], dtype=dtype)

@parameters_as_numpy_arrays('points')
def create_from_points(points, dtype=None):
    """Creates a sphere centred around 0,0,0 that encompasses
    the furthest point in the provided list.

    :param numpy.array points: An Nd array of vectors.
    :rtype: A sphere as a two value tuple.
    """
    dtype = dtype or points.dtype
    # calculate the lengths of all the points
    # use squared length to save processing
    lengths = np.apply_along_axis(
        np.sum,
        points.ndim - 1,
        points**2
    )

    # find the maximum value
    maximum = lengths.max()

    # square root this, this is the radius
    radius = np.sqrt(maximum)
    return np.array([0.0, 0.0, 0.0, radius], dtype=dtype)

@all_parameters_as_numpy_arrays
def position(sphere):
    """Returns the position of the sphere.

    :param numpy.array sphere: The sphere to extract the position from.
    :rtype: numpy.array
    :return: The centre of the sphere.
    """
    return sphere[:3].copy()

@all_parameters_as_numpy_arrays
def radius(sphere):
    """Returns the radius of the sphere.

    :param numpy.array sphere: The sphere to extract the radius from.
    :rtype: float
    :return: The radius of the sphere.
    """
    return sphere[3]

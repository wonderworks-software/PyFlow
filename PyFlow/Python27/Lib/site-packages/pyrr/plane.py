# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Planes.

Planes are represented using a numpy.array of shape (4,).
The values represent the plane equation using the values A,B,C,D.

The first three values are the normal vector.
The fourth value is the distance of the plane from the origin, down the normal.

.. seealso: http://en.wikipedia.org/wiki/Plane_(geometry)
.. seealso: http://mathworld.wolfram.com/Plane.html
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import vector
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


def create(normal=None, distance=0.0, dtype=None):
    """Creates a plane that runs along the X,Y plane.

    It crosses the origin with a normal of 0,0,1 (+Z).

    :rtype: numpy.array
    :return: A plane that runs along the X,Y plane.
    """
    if normal is None:
        normal = [0.0, 0.0, 1.0]
    return np.array([normal[0], normal[1], normal[2], distance], dtype=dtype)

@parameters_as_numpy_arrays('vector1', 'vector2', 'vector3')
def create_from_points(vector1, vector2, vector3, dtype=None):
    """Create a plane from 3 co-planar vectors.

    The vectors must all lie on the same
    plane or an exception will be thrown.

    The vectors must not all be in a single line or
    the plane is undefined.

    The order the vertices are passed in will determine the
    normal of the plane.

    :param numpy.array vector1: a vector that lies on the desired plane.
    :param numpy.array vector2: a vector that lies on the desired plane.
    :param numpy.array vector3: a vector that lies on the desired plane.
    :raise ValueError: raised if the vectors are co-incident (in a single line).
    :rtype: numpy.array
    :return: A plane that contains the 3 specified vectors.
    """
    dtype = dtype or vector1.dtype

    # make the vectors relative to vector2
    relV1 = vector1 - vector2
    relV2 = vector3 - vector2

    # cross our relative vectors
    normal = np.cross(relV1, relV2)
    if np.count_nonzero(normal) == 0:
        raise ValueError("Vectors are co-incident")

    # create our plane
    return create_from_position(position=vector2, normal=normal, dtype=dtype)

@parameters_as_numpy_arrays('position', 'normal')
def create_from_position(position, normal, dtype=None):
    """Creates a plane at position with the normal being above the plane
    and up being the rotation of the plane.

    :param numpy.array position: The position of the plane.
    :param numpy.array normal: The normal of the plane. Will be normalized
        during construction.
    :rtype: numpy.array
    :return: A plane that crosses the specified position with the specified
        normal.
    """
    dtype = dtype or position.dtype
    # -d = a * px  + b * py + c * pz
    n = vector.normalize(normal)
    d = -np.sum(n * position)
    return create(n, d, dtype)

def create_xy(invert=False, distance=0., dtype=None):
    """Create a plane on the XY plane, starting at the origin with +Z being
    the up vector.

    The distance is the distance along the normal (-Z if inverted, otherwise +Z).
    """
    invert = -1. if invert else 1.
    return np.array([0., 0., 1. * invert, distance])

def create_xz(invert=False, distance=0., dtype=None):
    """Create a plane on the XZ plane, starting at the origin with +Y being
    the up vector.

    The distance is the distance along the normal (-Y if inverted, otherwise +Y).
    """
    invert = -1. if invert else 1.
    return np.array([0., 1. * invert, 0., distance])

def create_yz(invert=False, distance=0., dtype=None):
    """Create a plane on the YZ plane, starting at the origin with +X being
    the up vector.

    The distance is the distance along the normal (-X if inverted, otherwise +X).
    """
    invert = -1. if invert else 1.
    return np.array([1. * invert, 0., 0., distance])

def invert_normal(plane):
    """Flips the normal of the plane.

    The plane is **not** changed in place.

    :rtype: numpy.array
    :return: The plane with the normal inverted.
    """
    # flip the normal, and the distance
    return -plane

def position(plane):
    """Extracts the position vector from a plane.

    This will be a vector co-incident with the plane's normal.

    :param numpy.array plane: The plane.
    :rtype: numpy.array
    :return: A valid position that lies on the plane.
    """
    return plane[:3] * plane[3]

def normal(plane):
    """Extracts the normal vector from a plane.

    :param numpy.array plane: The plane.
    :rtype: numpy.array
    :return: The normal vector of the plane.
    """
    return plane[:3].copy()

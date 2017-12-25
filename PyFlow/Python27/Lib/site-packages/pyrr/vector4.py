# -*- coding: utf-8 -*-
"""Provides functions for creating and manipulating 4D vectors.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import parameters_as_numpy_arrays

# import common vector operations
from .vector import *


def create(x=0., y=0., z=0., w=0.0, dtype=None):
    if isinstance(x, (list, np.ndarray)):
        raise ValueError('Function requires non-list arguments')
    return np.array([x,y,z,w], dtype=dtype)

def create_unit_length_x(dtype=None):
    return np.array([1.0, 0.0, 0.0, 0.0], dtype=dtype)

def create_unit_length_y(dtype=None):
    return np.array([0.0, 1.0, 0.0, 0.0], dtype=dtype)

def create_unit_length_z(dtype=None):
    return np.array([0.0, 0.0, 1.0, 0.0], dtype=dtype)

def create_unit_length_w(dtype=None):
    return np.array([0.0, 0.0, 0.0, 1.0], dtype=dtype)

@parameters_as_numpy_arrays('vector')
def create_from_vector3(vector, w=0., dtype=None):
    dtype = dtype or vector.dtype
    return np.array([vector[0], vector[1], vector[2], w], dtype=dtype)

@parameters_as_numpy_arrays('mat')
def create_from_matrix44_translation(mat, dtype=None):
    return np.array(mat[3, :4], dtype=dtype)

class index:
    #: The index of the X value within the vector
    x = 0

    #: The index of the Y value within the vector
    y = 1

    #: The index of the Z value within the vector
    z = 2

    #: The index of the W value within the vector
    w = 3


class unit:
    #: A vector of unit length in the X-axis. (1.0, 0.0, 0.0, 0.0)
    x = create_unit_length_x()

    #: A vector of unit length in the Y-axis. (0.0, 1.0, 0.0, 0.0)
    y = create_unit_length_y()

    #: A vector of unit length in the Z-axis. (0.0, 0.0, 1.0, 0.0)
    z = create_unit_length_z()

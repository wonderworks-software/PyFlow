# -*- coding: utf-8 -*-
"""Common Vector manipulation functions.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


@all_parameters_as_numpy_arrays
def normalize(vec):
    """normalizes an Nd list of vectors or a single vector
    to unit length.

    The vector is **not** changed in place.

    For zero-length vectors, the result will be np.nan.

    :param numpy.array vec: an Nd array with the final dimension
        being vectors
        ::

            numpy.array([ x, y, z ])

        Or an NxM array::

            numpy.array([
                [x1, y1, z1],
                [x2, y2, z2]
            ]).

    :rtype: A numpy.array the normalized value
    """
    # calculate the length
    # this is a duplicate of length(vec) because we
    # always want an array, even a 0-d array.
    return (vec.T  / np.sqrt(np.sum(vec**2,axis=-1))).T



@all_parameters_as_numpy_arrays
def normalise(vec):    # TODO: mark as deprecated
    """normalizes an Nd list of vectors or a single vector
    to unit length.

    The vector is **not** changed in place.

    For zero-length vectors, the result will be np.nan.

    :param numpy.array vec: an Nd array with the final dimension
        being vectors
        ::

            numpy.array([ x, y, z ])

        Or an NxM array::

            numpy.array([
                [x1, y1, z1],
                [x2, y2, z2]
            ]).

    :rtype: A numpy.array the normalized value
    """
    # calculate the length
    # this is a duplicate of length(vec) because we
    # always want an array, even a 0-d array.
    return (vec.T  / np.sqrt(np.sum(vec**2,axis=-1))).T



@all_parameters_as_numpy_arrays
def squared_length(vec):
    """Calculates the squared length of a vector.

    Useful when trying to avoid the performance
    penalty of a square root operation.

    :param numpy.array vec: An Nd numpy.array.
    :rtype: If one vector is supplied, the result with be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    lengths = np.sum(vec ** 2., axis=-1)

    return lengths

@all_parameters_as_numpy_arrays
def length(vec):
    """Returns the length of an Nd list of vectors
    or a single vector.

    :param numpy.array vec: an Nd array with the final dimension
        being size 3 (a vector).

        Single vector::

            numpy.array([ x, y, z ])

        Nd array::

            numpy.array([
                [x1, y1, z1],
                [x2, y2, z2]
            ]).

    :rtype: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return np.sqrt(np.sum(vec**2,axis=-1))


@parameters_as_numpy_arrays('vec')
def set_length(vec, len):
    """Resizes an Nd list of vectors or a single vector to 'length'.

    The vector is **not** changed in place.

    :param numpy.array vec: an Nd array with the final dimension
        being size 3 (a vector).

        Single vector::
            numpy.array([ x, y, z ])

        Nd array::
            numpy.array([
                [x1, y1, z1],
                [x2, y2, z2]
            ]).

    :rtype: A numpy.array of shape vec.shape.
    """
    # calculate the length
    # this is a duplicate of length(vec) because we
    # always want an array, even a 0-d array.

    return (vec.T  / np.sqrt(np.sum(vec**2,axis=-1)) * len).T


@all_parameters_as_numpy_arrays
def dot(v1, v2):
    """Calculates the dot product of two vectors.

    :param numpy.array v1: an Nd array with the final dimension
        being size 3. (a vector)
    :param numpy.array v2: an Nd array with the final dimension
        being size 3 (a vector)
    :rtype: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return np.sum(v1 * v2, axis=-1)

@parameters_as_numpy_arrays('v1', 'v2')
def interpolate(v1, v2, delta):
    """Interpolates between 2 arrays of vectors (shape = N,3)
    by the specified delta (0.0 <= delta <= 1.0).

    :param numpy.array v1: an Nd array with the final dimension
        being size 3. (a vector)
    :param numpy.array v2: an Nd array with the final dimension
        being size 3. (a vector)
    :param float delta: The interpolation percentage to apply,
        where 0.0 <= delta <= 1.0.
        When delta is 0.0, the result will be v1.
        When delta is 1.0, the result will be v2.
        Values inbetween will be an interpolation.
    :rtype: A numpy.array with shape v1.shape.
    """
    # scale the difference based on the time
    # we must do it this 'unreadable' way to avoid
    # loss of precision.
    # the 'readable' method (f_now = f_0 + (f1 - f0) * delta)
    # causes floating point errors due to the small values used
    # in md2 files and the values become corrupted.
    # this horrible code curtousey of this comment:
    # http://stackoverflow.com/questions/5448322/temporal-interpolation-in-numpy-matplotlib
    return v1 + ((v2 - v1) * delta)
    #return v1 * (1.0 - delta ) + v2 * delta
    t = delta
    t0 = 0.0
    t1 = 1.0
    delta_t = t1 - t0
    return (t1 - t) / delta_t * v1 + (t - t0) / delta_t * v2

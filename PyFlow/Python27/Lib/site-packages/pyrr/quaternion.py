# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Quaternions.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import vector, vector3, vector4
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


class index:
    #: The index of the X value within the quaternion
    x = 0

    #: The index of the Y value within the quaternion
    y = 1

    #: The index of the Z value within the quaternion
    z = 2

    #: The index of the W value within the quaternion
    w = 3


def create(x=0., y=0., z=0., w=1., dtype=None):
    return np.array([x, y, z, w], dtype=dtype)

def create_from_x_rotation(theta, dtype=None):
    thetaOver2 = theta * 0.5

    return np.array(
        [
            np.sin(thetaOver2),
            0.0,
            0.0,
            np.cos(thetaOver2)
        ],
        dtype=dtype
    )

def create_from_y_rotation(theta, dtype=None):
    thetaOver2 = theta * 0.5

    return np.array(
        [
            0.0,
            np.sin(thetaOver2),
            0.0,
            np.cos(thetaOver2)
        ],
        dtype=dtype
    )

def create_from_z_rotation(theta, dtype=None):
    thetaOver2 = theta * 0.5

    return np.array(
        [
            0.0,
            0.0,
            np.sin(thetaOver2),
            np.cos(thetaOver2)
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('axis')
def create_from_axis_rotation(axis, theta, dtype=None):
    dtype = dtype or axis.dtype
    # make sure the vector is normalized
    if not np.isclose(np.linalg.norm(axis), 1.):
        axis = vector.normalize(axis)

    thetaOver2 = theta * 0.5
    sinThetaOver2 = np.sin(thetaOver2)

    return np.array(
        [
            sinThetaOver2 * axis[0],
            sinThetaOver2 * axis[1],
            sinThetaOver2 * axis[2],
            np.cos(thetaOver2)
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('mat')
def create_from_matrix(mat, dtype=None):
    # http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm
    # optimised "alternative version" does not produce correct results
    # see issue #42
    dtype = dtype or mat.dtype

    trace = mat[0][0] + mat[1][1] + mat[2][2]
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        qx = (mat[2][1] - mat[1][2]) * s
        qy = (mat[0][2] - mat[2][0]) * s
        qz = (mat[1][0] - mat[0][1]) * s
        qw = 0.25 / s
    elif mat[0][0] > mat[1][1] and mat[0][0] > mat[2][2]:
        s = 2.0 * np.sqrt(1.0 + mat[0][0] - mat[1][1] - mat[2][2])
        qx = 0.25 * s
        qy = (mat[0][1] + mat[1][0]) / s
        qz = (mat[0][2] + mat[2][0]) / s
        qw = (mat[2][1] - mat[1][2]) / s
    elif mat[1][1] > mat[2][2]:
        s = 2.0 * np.sqrt(1.0 + mat[1][1] - mat[0][0] - mat[2][2])
        qx = (mat[0][1] + mat[1][0]) / s
        qy = 0.25 * s
        qz = (mat[1][2] + mat[2][1]) / s
        qw = (mat[0][2] - mat[2][0]) / s
    else:
        s = 2.0 * np.sqrt(1.0 + mat[2][2] - mat[0][0] - mat[1][1])
        qx = (mat[0][2] + mat[2][0]) / s
        qy = (mat[1][2] + mat[2][1]) / s
        qz = 0.25 * s
        qw = (mat[1][0] - mat[0][1]) / s

    quat = np.array([qx, qy, qz, qw], dtype=dtype)
    return quat

@parameters_as_numpy_arrays('eulers')
def create_from_eulers(eulers, dtype=None):
    """Creates a quaternion from a set of Euler angles.

    Eulers are an array of length 3 in the following order::
        [yaw, pitch, roll]
    """
    dtype = dtype or eulers.dtype

    pitch, yaw, roll = eulers

    halfPitch = pitch * 0.5
    sP = np.sin(halfPitch)
    cP = np.cos(halfPitch)

    halfRoll = roll * 0.5
    sR = np.sin(halfRoll)
    cR = np.cos(halfRoll)

    halfYaw = yaw * 0.5
    sY = np.sin(halfYaw)
    cY = np.cos(halfYaw)

    return np.array(
        [
            # x = -cy * sp * cr - sy * cp * sr
            (-cY * sP * cR) - (sY * cP * sR),
            # y = cy * sp * sr - sy * cp * cr
            (cY * sP * sR) - (sY * cP * cR),
            # z = sy * sp * cr - cy * cp * sr
            (sY * sP * cR) - (cY * cP * sR),
            # w = cy * cp * cr + sy * sp * sr
            (cY * cP * cR) + (sY * sP * sR),
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('axis')
def create_from_inverse_of_eulers(eulers, dtype=None):
    """Creates a quaternion from the inverse of a set of Euler angles.

    Eulers are an array of length 3 in the following order::
        [yaw, pitch, roll]
    """
    dtype = dtype or eulers.dtype

    pitch, roll, yaw = euler.pitch(eulers), euler.roll(eulers), euler.yaw(eulers)

    halfRoll = roll * 0.5
    sinRoll = np.sin(halfRoll)
    cosRoll = np.cos(halfRoll)

    halfPitch = pitch * 0.5
    sinPitch = np.sin(halfPitch)
    cosPitch = np.cos(halfPitch)

    halfYaw = yaw * 0.5
    sinYaw = np.sin(halfYaw)
    cosYaw = np.cos(halfYaw)

    return np.array(
        [
            # x = cy * sp * cr + sy * cp * sr
            (cosYaw * sinPitch * cosRoll) + (sinYaw * cosPitch * sinRoll),
            # y = -cy * sp * sr + sy * cp * cr
            (-cosYaw * sinPitch * sinRoll) + (sinYaw * cosPitch * cosRoll),
            # z = -sy * sp * cr + cy * cp * sr
            (-sinYaw * sinPitch * cosRoll) + (cosYaw * cosPitch * sinRoll),
            # w = cy * cp * cr + sy * sp * sr
            (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll)
        ],
        dtype=dtype
    )

@all_parameters_as_numpy_arrays
def cross(quat1, quat2):
    """Returns the cross-product of the two quaternions.

    Quaternions are **not** communicative. Therefore, order is important.

    This is NOT the same as a vector cross-product.
    Quaternion cross-product is the equivalent of matrix multiplication.
    """
    q1x, q1y, q1z, q1w = quat1
    q2x, q2y, q2z, q2w = quat2

    return np.array(
        [
             q1x * q2w + q1y * q2z - q1z * q2y + q1w * q2x,
            -q1x * q2z + q1y * q2w + q1z * q2x + q1w * q2y,
             q1x * q2y - q1y * q2x + q1z * q2w + q1w * q2z,
            -q1x * q2x - q1y * q2y - q1z * q2z + q1w * q2w,
        ],
        dtype=quat1.dtype
    )

def lerp(quat1, quat2, t):
    """Interpolates between quat1 and quat2 by t.
    The parameter t is clamped to the range [0, 1]
    """

    quat1 = np.asarray(quat1)
    quat2 = np.asarray(quat2)

    t = np.clip(t, 0, 1)
    return normalize(quat1 * (1 - t) + quat2 * t)

def slerp(quat1, quat2, t):
    """Spherically interpolates between quat1 and quat2 by t.
    The parameter t is clamped to the range [0, 1]
    """

    quat1 = np.asarray(quat1)
    quat2 = np.asarray(quat2)

    t = np.clip(t, 0, 1)
    dot = vector4.dot(quat1, quat2)

    if dot < 0.0:
        dot = -dot
        quat3 = -quat2

    else:
        quat3 = quat2

    if dot < 0.95:
        angle = np.arccos(dot)
        res = (quat1 * np.sin(angle * (1 - t)) + quat3 * np.sin(angle * t)) / np.sin(angle)

    else:
        res = lerp(quat1, quat2, t)

    return res

def is_zero_length(quat):
    """Checks if a quaternion is zero length.

    :param numpy.array quat: The quaternion to check.
    :rtype: boolean.
    :return: True if the quaternion is zero length, otherwise False.
    """
    return quat[0] == quat[1] == quat[2] == quat[3] == 0.0

def is_non_zero_length(quat):
    """Checks if a quaternion is not zero length.

    This is the opposite to 'is_zero_length'.
    This is provided for readability.

    :param numpy.array quat: The quaternion to check.
    :rtype: boolean
    :return: False if the quaternion is zero length, otherwise True.

    .. seealso:: is_zero_length
    """
    return not is_zero_length(quat)

def squared_length(quat):
    """Calculates the squared length of a quaternion.

    Useful for avoiding the performanc penalty of
    the square root function.

    :param numpy.array quat: The quaternion to measure.
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector4.squared_length(quat)

def length(quat):
    """Calculates the length of a quaternion.

    :param numpy.array quat: The quaternion to measure.
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector4.length(quat)

def normalize(quat):
    """Ensure a quaternion is unit length (length ~= 1.0).

    The quaternion is **not** changed in place.

    :param numpy.array quat: The quaternion to normalize.
    :rtype: numpy.array
    :return: The normalized quaternion(s).
    """
    return vector4.normalize(quat)

def normalise(quat):    # TODO: mark as deprecated
    """Ensure a quaternion is unit length (length ~= 1.0).

    The quaternion is **not** changed in place.

    :param numpy.array quat: The quaternion to normalize.
    :rtype: numpy.array
    :return: The normalized quaternion(s).
    """
    return vector4.normalize(quat)

def rotation_angle(quat):
    """Calculates the rotation around the quaternion's axis.

    :param numpy.array quat: The quaternion.
    :rtype: float.
    :return: The quaternion's rotation about the its axis in radians.
    """
    # extract the W component
    thetaOver2 = np.arccos(quat[3])
    return thetaOver2 * 2.0

@all_parameters_as_numpy_arrays
def rotation_axis(quat):
    """Calculates the axis of the quaternion's rotation.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array.
    :return: The quaternion's rotation axis.
    """
    # extract W component
    sinThetaOver2Sq = 1.0 - (quat[3] ** 2)

    # check for zero before we sqrt
    if sinThetaOver2Sq <= 0.0:
        # identity quaternion or numerical imprecision.
        # return a valid vector
        # we'll treat -Z as the default
        return np.array([0.0, 0.0, -1.0], dtype=quat.dtype)

    oneOverSinThetaOver2 = 1.0 / np.sqrt(sinThetaOver2Sq)

    # we use the x,y,z values
    return np.array(
        [
            quat[0] * oneOverSinThetaOver2,
            quat[1] * oneOverSinThetaOver2,
            quat[2] * oneOverSinThetaOver2
        ],
        dtype=quat.dtype
    )

def dot(quat1, quat2):
    """Calculate the dot product of quaternions.

    This is the same as a vector dot product.

    :param numpy.array quat1: The first quaternion(s).
    :param numpy.array quat2: The second quaternion(s).
    :rtype: float, numpy.array
    :return: If a 1d array was passed, it will be a scalar.
        Otherwise the result will be an array of scalars with shape
        vec.ndim with the last dimension being size 1.
    """
    return vector4.dot(quat1, quat2)

@all_parameters_as_numpy_arrays
def conjugate(quat):
    """Calculates a quaternion with the opposite rotation.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array.
    :return: A quaternion representing the conjugate.
    """

    # invert x,y,z and leave w as is
    return np.array(
        [
            -quat[0],
            -quat[1],
            -quat[2],
            quat[3]
        ],
        dtype=quat.dtype
    )

@parameters_as_numpy_arrays('quat')
def power(quat, exponent):
    """Multiplies the quaternion by the exponent.

    The quaternion is **not** changed in place.

    :param numpy.array quat: The quaternion.
    :param float scalar: The exponent.
    :rtype: numpy.array.
    :return: A quaternion representing the original quaternion
        to the specified power.
    """
    # check for identify quaternion
    if np.fabs(quat[3]) > 0.9999:
        # assert for the time being
        assert False
        print("rotation axis was identity")

        return quat

    alpha = np.arccos(quat[3])
    newAlpha = alpha * exponent
    multi = np.sin(newAlpha) / np.sin(alpha)

    return np.array(
        [
            quat[0] * multi,
            quat[1] * multi,
            quat[2] * multi,
            np.cos(newAlpha)
        ],
        dtype=quat.dtype
    )

def inverse(quat):
    """Calculates the inverse quaternion.

    The inverse of a quaternion is defined as
    the conjugate of the quaternion divided
    by the magnitude of the original quaternion.

    :param numpy.array quat: The quaternion to invert.
    :rtype: numpy.array.
    :return: The inverse of the quaternion.
    """
    return conjugate(quat) / length(quat)

@all_parameters_as_numpy_arrays
def negate(quat):
    """Calculates the negated quaternion.

    This is essentially the quaternion * -1.0.

    :param numpy.array quat: The quaternion.
    :rtype: numpy.array
    :return: The negated quaternion.
    """
    return quat * -1.0

def is_identity(quat):
    return np.allclose(quat, [0.,0.,0.,1.])

@all_parameters_as_numpy_arrays
def apply_to_vector(quat, vec):
    """Rotates a vector by a quaternion.

    :param numpy.array quat: The quaternion.
    :param numpy.array vec: The vector.
    :rtype: numpy.array
    :return: The vector rotated by the quaternion.
    :raise ValueError: raised if the vector is an unsupported size

    .. seealso:: http://content.gpwiki.org/index.php/OpenGL:Tutorials:Using_Quaternions_to_represent_rotation
    """
    def apply(quat, vec4):
        result = cross(quat, cross(vec4, conjugate(quat)))
        return result

    if vec.size == 3:
        # convert to vector4
        # ignore w component by setting it to 0.
        vec = np.array([vec[0], vec[1], vec[2], 0.0], dtype=vec.dtype)
        vec = apply(quat, vec)
        vec = vec[:3]
        return vec
    elif vec.size == 4:
        vec = apply(quat, vec)
        return vec
    else:
        raise ValueError("Vector size unsupported")

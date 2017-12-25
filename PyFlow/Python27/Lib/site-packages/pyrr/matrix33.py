# -*- coding: utf-8 -*-
"""3x3 Matrix which supports rotation, translation, scale and skew.

Matrices are laid out in row-major format and can be loaded directly
into OpenGL.
To convert to column-major format, transpose the array using the
numpy.array.T method.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import vector, quaternion, euler
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


def create_identity(dtype=None):
    """Creates a new matrix33 and sets it to
    an identity matrix.

    :rtype: numpy.array
    :return: A matrix representing an identity matrix with shape (3,3).
    """
    return np.identity(3, dtype=dtype)

def create_from_matrix44(mat, dtype=None):
    """Creates a Matrix33 from a Matrix44.

    :rtype: numpy.array
    :return: A matrix with shape (3,3) with the input matrix rotation.
    """
    mat = np.asarray(mat)
    return np.array(mat[0:3,0:3], dtype=dtype)

@parameters_as_numpy_arrays('eulers')
def create_from_eulers(eulers, dtype=None):
    """Creates a matrix from the specified Euler rotations.

    :param numpy.array eulers: A set of euler rotations in the format
        specified by the euler modules.
    :rtype: numpy.array
    :return: A matrix with shape (3,3) with the euler's rotation.
    """
    dtype = dtype or eulers.dtype

    pitch, roll, yaw = euler.pitch(eulers), euler.roll(eulers), euler.yaw(eulers)

    sP = np.sin(pitch)
    cP = np.cos(pitch)
    sR = np.sin(roll)
    cR = np.cos(roll)
    sY = np.sin(yaw)
    cY = np.cos(yaw)

    return np.array(
        [
            # m1
            [
                cY * cP,
                -cY * sP * cR + sY * sR,
                cY * sP * sR + sY * cR,
            ],
            # m2
            [
                sP,
                cP * cR,
                -cP * sR,
            ],
            # m3
            [
                -sY * cP,
                sY * sP * cR + cY * sR,
                -sY * sP * sR + cY * cR,
            ]
        ],
        dtype=dtype
    )


@parameters_as_numpy_arrays('axis')
def create_from_axis_rotation(axis, theta, dtype=None):
    """Creates a matrix from the specified theta rotation around an axis.

    :param numpy.array axis: A (3,) vector specifying the axis of rotation.
    :param float theta: A rotation speicified in radians.
    :rtype: numpy.array
    :return: A matrix with shape (3,3).
    """
    dtype = dtype or axis.dtype

    axis = vector.normalize(axis)
    x,y,z = axis

    s = np.sin(theta);
    c = np.cos(theta);
    t = 1 - c;

    # Construct the elements of the rotation matrix
    return np.array(
        [
            [ x * x * t + c,     y * x * t + z * s, z * x * t - y * s],
            [ x * y * t - z * s, y * y * t + c,     z * y * t + x * s],
            [ x * z * t + y * s, y * z * t - x * s, z * z * t + c]
        ],
        dtype= dtype
    )


@parameters_as_numpy_arrays('quat')
def create_from_quaternion(quat, dtype=None):
    """Creates a matrix with the same rotation as a quaternion.

    :param quat: The quaternion to create the matrix from.
    :rtype: numpy.array
    :return: A matrix with shape (3,3) with the quaternion's rotation.
    """
    dtype = dtype or quat.dtype

    # the quaternion must be normalized
    if not np.isclose(np.linalg.norm(quat), 1.):
        quat = quaternion.normalize(quat)

    # http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
    qx, qy, qz, qw = quat[0], quat[1], quat[2], quat[3]

    sqw = qw**2
    sqx = qx**2
    sqy = qy**2
    sqz = qz**2
    qxy = qx * qy
    qzw = qz * qw
    qxz = qx * qz
    qyw = qy * qw
    qyz = qy * qz
    qxw = qx * qw

    invs = 1 / (sqx + sqy + sqz + sqw)
    m00 = ( sqx - sqy - sqz + sqw) * invs
    m11 = (-sqx + sqy - sqz + sqw) * invs
    m22 = (-sqx - sqy + sqz + sqw) * invs
    m10 = 2.0 * (qxy + qzw) * invs
    m01 = 2.0 * (qxy - qzw) * invs
    m20 = 2.0 * (qxz - qyw) * invs
    m02 = 2.0 * (qxz + qyw) * invs
    m21 = 2.0 * (qyz + qxw) * invs
    m12 = 2.0 * (qyz - qxw) * invs

    return np.array([
        [m00, m01, m02],
        [m10, m11, m12],
        [m20, m21, m22],
    ], dtype=dtype)


@parameters_as_numpy_arrays('quat')
def create_from_inverse_of_quaternion(quat, dtype=None):
    """Creates a matrix with the inverse rotation of a quaternion.

    :param numpy.array quat: The quaternion to make the matrix from (shape 4).
    :rtype: numpy.array
    :return: A matrix with shape (3,3) that respresents the inverse of
        the quaternion.
    """
    dtype = dtype or quat.dtype

    x, y, z, w = quat

    x2 = x**2
    y2 = y**2
    z2 = z**2
    wx = w * x
    wy = w * y
    xy = x * y
    wz = w * z
    xz = x * z
    yz = y * z

    return np.array(
        [
            # m1
            [
                # m11 = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
                1.0 - 2.0 * (y2 + z2),
                # m21 = 2.0 * (q.x * q.y + q.w * q.z)
                2.0 * (xy + wz),
                # m31 = 2.0 * (q.x * q.z - q.w * q.y)
                2.0 * (xz - wy),
            ],
            # m2
            [
                # m12 = 2.0 * (q.x * q.y - q.w * q.z)
                2.0 * (xy - wz),
                # m22 = 1.0 - 2.0 * (q.x * q.x + q.z * q.z)
                1.0 - 2.0 * (x2 + z2),
                # m32 = 2.0 * (q.y * q.z + q.w * q.x)
                2.0 * (yz + wx),
            ],
            # m3
            [
                # m13 = 2.0 * ( q.x * q.z + q.w * q.y)
                2.0 * (xz + wy),
                # m23 = 2.0 * (q.y * q.z - q.w * q.x)
                2.0 * (yz - wx),
                # m33 = 1.0 - 2.0 * (q.x * q.x + q.y * q.y)
                1.0 - 2.0 * (x2 + y2),
            ]
        ],
        dtype=dtype
    )

def create_from_scale(scale, dtype=None):
    """Creates an identity matrix with the scale set.

    :param numpy.array scale: The scale to apply as a vector (shape 3).
    :rtype: numpy.array
    :return: A matrix with shape (3,3) with the scale
        set to the specified vector.
    """
    # apply the scale to the values diagonally
    # down the matrix
    m = np.diagflat(scale)
    if dtype:
        m = m.astype(dtype)
    return m

def create_from_x_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the X axis.

    :param float theta: The rotation, in radians, about the X-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (3,3) with the specified rotation about
        the X-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    cosT = np.cos(theta)
    sinT = np.sin(theta)

    return np.array(
        [
            [ 1.0, 0.0, 0.0 ],
            [ 0.0, cosT,-sinT ],
            [ 0.0, sinT, cosT ]
        ],
        dtype=dtype
    )

def create_from_y_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Y axis.

    :param float theta: The rotation, in radians, about the Y-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (3,3) with the specified rotation about
        the Y-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    cosT = np.cos(theta)
    sinT = np.sin(theta)

    return np.array(
        [
            [ cosT, 0.0,sinT ],
            [ 0.0, 1.0, 0.0 ],
            [-sinT, 0.0, cosT ]
        ],
        dtype=dtype
    )

def create_from_z_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Z axis.

    :param float theta: The rotation, in radians, about the Z-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (3,3) with the specified rotation about
        the Z-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    cosT = np.cos(theta)
    sinT = np.sin(theta)

    return np.array(
        [
            [ cosT,-sinT, 0.0 ],
            [ sinT, cosT, 0.0 ],
            [ 0.0, 0.0, 1.0 ]
        ],
        dtype=dtype
    )

@parameters_as_numpy_arrays('vec')
def apply_to_vector(mat, vec):
    """Apply a matrix to a vector.

    The matrix's rotation are applied to the vector.
    Supports multiple matrices and vectors.

    :param numpy.array mat: The rotation / translation matrix.
        Can be a list of matrices.
    :param numpy.array vec: The vector to modify.
        Can be a list of vectors.
    :rtype: numpy.array
    :return: The vectors rotated by the specified matrix.
    """
    if vec.size == 3:
        return np.dot(vec, mat)
    else:
        raise ValueError("Vector size unsupported")

def multiply(m1, m2):
    """Multiply two matricies, m1 . m2.

    This is essentially a wrapper around
    numpy.dot( m1, m2 )

    :param numpy.array m1: The first matrix.
        Can be a list of matrices.
    :param numpy.array m2: The second matrix.
        Can be a list of matrices.
    :rtype: numpy.array
    :return: A matrix that results from multiplying m1 by m2.
    """
    return np.dot(m1, m2)

def inverse(mat):
    """Returns the inverse of the matrix.

    This is essentially a wrapper around numpy.linalg.inv.

    :param numpy.array m: A matrix.
    :rtype: numpy.array
    :return: The inverse of the specified matrix.

    .. seealso:: http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.inv.html
    """
    return np.linalg.inv(mat)

def create_direction_scale(direction, scale):
    """Creates a matrix which can apply a directional scaling to a set of vectors.

    An example usage for this is to flatten a mesh against a
    single plane.

    :param numpy.array direction: a numpy.array of shape (3,) of the direction to scale.
    :param float scale: a float value for the scaling along the specified direction.
        A scale of 0.0 will flatten the vertices into a single plane with the direction being the
        plane's normal.
    :rtype: numpy.array
    :return: The scaling matrix.
    """
    """
    scaling is defined as:

    [p'][1 + (k - 1)n.x^2, (k - 1)n.x n.y^2, (k - 1)n.x n.z   ]
    S(n,k) = [q'][(k - 1)n.x n.y,   1 + (k - 1)n.y,   (k - 1)n.y n.z   ]
    [r'][(k - 1)n.x n.z,   (k - 1)n.y n.z,   1 + (k - 1)n.z^2 ]

    where:
    v' is the resulting vector after scaling
    v is the vector to scale
    n is the direction of the scaling
    n.x is the x component of n
    n.y is the y component of n
    n.z is the z component of n
    k is the scaling factor
    """
    if not np.isclose(np.linalg.norm(direction), 1.):
        direction = vector.normalize(direction)

    x,y,z = direction

    x2 = x**2.
    y2 = y**2.
    z2 = z**2

    scaleMinus1 = scale - 1.
    return np.array(
        [
            # m1
            [
                # m11 = 1 + (k - 1)n.x^2
                1. + scaleMinus1 * x2,
                # m12 = (k - 1)n.x n.y^2
                scaleMinus1 * x * y2,
                # m13 = (k - 1)n.x n.z
                scaleMinus1 * x * z
            ],
            # m2
            [
                # m21 = (k - 1)n.x n.y
                scaleMinus1 * x * y,
                # m22 = 1 + (k - 1)n.y
                1. + scaleMinus1 * y,
                # m23 = (k - 1)n.y n.z
                scaleMinus1 * y * z
            ],
            # m3
            [
                # m31 = (k - 1)n.x n.z
                scaleMinus1 * x * z,
                # m32 = (k - 1)n.y n.z
                scaleMinus1 * y * z,
                # m33 = 1 + (k - 1)n.z^2
                1. + scaleMinus1 * z2
            ]
        ]
    )

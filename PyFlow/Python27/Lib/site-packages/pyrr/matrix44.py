# -*- coding: utf-8 -*-
"""4x4 Matrix which supports rotation, translation, scale and skew.

Matrices are laid out in row-major format and can be loaded directly
into OpenGL.
To convert to column-major format, transpose the array using the
numpy.array.T method.
"""
from __future__ import absolute_import, division, print_function
import numpy as np
from . import matrix33
from . import vector
from .utils import all_parameters_as_numpy_arrays, parameters_as_numpy_arrays


def create_identity(dtype=None):
    """Creates a new matrix44 and sets it to
    an identity matrix.

    :rtype: numpy.array
    :return: A matrix representing an identity matrix with shape (4,4).
    """
    return np.identity(4, dtype=dtype)

def create_from_matrix33(mat, dtype=None):
    """Creates a Matrix44 from a Matrix33.

    The translation will be 0,0,0.

    :rtype: numpy.array
    :return: A matrix with shape (4,4) with the input matrix rotation.
    """
    mat4 = np.identity(4, dtype=dtype)
    mat4[0:3, 0:3] = mat
    return mat4

def create_matrix33_view(mat):
    """Returns a view into the matrix in Matrix33 format.

    This is different from matrix33.create_from_matrix44, in that
    changes to the returned matrix will also alter the original matrix.

    :rtype: numpy.array
    :return: A view into the matrix in the format of a matrix33 (shape (3,3)).
    """
    return mat[0:3, 0:3]

@parameters_as_numpy_arrays('eulers')
def create_from_eulers(eulers, dtype=None):
    """Creates a matrix from the specified Euler rotations.

    :param numpy.array eulers: A set of euler rotations in the format
        specified by the euler modules.
    :rtype: numpy.array
    :return: A matrix with shape (4,4) with the euler's rotation.
    """
    dtype = dtype or eulers.dtype
    # set to identity matrix
    # this will populate our extra rows for us
    mat = create_identity(dtype)

    # we'll use Matrix33 for our conversion
    mat[0:3, 0:3] = matrix33.create_from_eulers(eulers, dtype)
    return mat

@parameters_as_numpy_arrays('axis')
def create_from_axis_rotation(axis, theta, dtype=None):
    """Creates a matrix from the specified rotation theta around an axis.

    :param numpy.array axis: A (3,) vector.
    :param float theta: A rotation in radians.

    :rtype: numpy.array
    :return: A matrix with shape (4,4).
    """
    dtype = dtype or axis.dtype
    # set to identity matrix
    # this will populate our extra rows for us
    mat = create_identity(dtype)

    # we'll use Matrix33 for our conversion
    mat[0:3, 0:3] = matrix33.create_from_axis_rotation(axis, theta, dtype)
    return mat

@parameters_as_numpy_arrays('quat')
def create_from_quaternion(quat, dtype=None):
    """Creates a matrix with the same rotation as a quaternion.

    :param quat: The quaternion to create the matrix from.
    :rtype: numpy.array
    :return: A matrix with shape (4,4) with the quaternion's rotation.
    """
    dtype = dtype or quat.dtype
    # set to identity matrix
    # this will populate our extra rows for us
    mat = create_identity(dtype)

    # we'll use Matrix33 for our conversion
    mat[0:3, 0:3] = matrix33.create_from_quaternion(quat, dtype)
    return mat

@parameters_as_numpy_arrays('quat')
def create_from_inverse_of_quaternion(quat, dtype=None):
    """Creates a matrix with the inverse rotation of a quaternion.

    This can be used to go from object space to intertial space.

    :param numpy.array quat: The quaternion to make the matrix from (shape 4).
    :rtype: numpy.array
    :return: A matrix with shape (4,4) that respresents the inverse of
        the quaternion.
    """
    dtype = dtype or quat.dtype
    # set to identity matrix
    # this will populate our extra rows for us
    mat = create_identity(dtype)

    # we'll use Matrix33 for our conversion
    mat[0:3, 0:3] = matrix33.create_from_inverse_of_quaternion(quat, dtype)
    return mat

@parameters_as_numpy_arrays('vec')
def create_from_translation(vec, dtype=None):
    """Creates an identity matrix with the translation set.

    :param numpy.array vec: The translation vector (shape 3 or 4).
    :rtype: numpy.array
    :return: A matrix with shape (4,4) that represents a matrix
        with the translation set to the specified vector.
    """
    dtype = dtype or vec.dtype
    mat = create_identity(dtype)
    mat[3, 0:3] = vec[:3]
    return mat

def create_from_scale(scale, dtype=None):
    """Creates an identity matrix with the scale set.

    :param numpy.array scale: The scale to apply as a vector (shape 3).
    :rtype: numpy.array
    :return: A matrix with shape (4,4) with the scale
        set to the specified vector.
    """
    # we need to expand 'scale' into it's components
    # because numpy isn't flattening them properly.
    m = np.diagflat([scale[0], scale[1], scale[2], 1.0])
    if dtype:
        m = m.astype(dtype)
    return m

def create_from_x_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the X axis.

    :param float theta: The rotation, in radians, about the X-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (4,4) with the specified rotation about
        the X-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    mat = create_identity(dtype)
    mat[0:3, 0:3] = matrix33.create_from_x_rotation(theta, dtype)
    return mat

def create_from_y_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Y axis.

    :param float theta: The rotation, in radians, about the Y-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (4,4) with the specified rotation about
        the Y-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    mat = create_identity(dtype)
    mat[0:3, 0:3] = matrix33.create_from_y_rotation(theta, dtype)
    return mat

def create_from_z_rotation(theta, dtype=None):
    """Creates a matrix with the specified rotation about the Z axis.

    :param float theta: The rotation, in radians, about the Z-axis.
    :rtype: numpy.array
    :return: A matrix with the shape (4,4) with the specified rotation about
        the Z-axis.

    .. seealso:: http://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
    """
    mat = create_identity(dtype)
    mat[0:3, 0:3] = matrix33.create_from_z_rotation(theta, dtype)
    return mat

@all_parameters_as_numpy_arrays
def apply_to_vector(mat, vec):
    """Apply a matrix to a vector.

    The matrix's rotation and translation are applied to the vector.
    Supports multiple matrices and vectors.

    :param numpy.array mat: The rotation / translation matrix.
        Can be a list of matrices.
    :param numpy.array vec: The vector to modify.
        Can be a list of vectors.
    :rtype: numpy.array
    :return: The vectors rotated by the specified matrix.
    """
    if vec.size == 3:
        # convert to a vec4
        vec4 = np.array([vec[0], vec[1], vec[2], 1.], dtype=vec.dtype)
        vec4 = np.dot(vec4, mat)
        if np.allclose(vec4[3], 0.):
            vec4[:] = [np.inf, np.inf, np.inf, np.inf]
        else:
            vec4 /= vec4[3]
        return vec4[:3]
    elif vec.size == 4:
        return np.dot(vec, mat)
    else:
        raise ValueError("Vector size unsupported")

def multiply(m1, m2):
    """Multiply two matricies, m1 . m2.

    This is essentially a wrapper around
    numpy.dot(m1, m2)

    :param numpy.array m1: The first matrix.
        Can be a list of matrices.
    :param numpy.array m2: The second matrix.
        Can be a list of matrices.
    :rtype: numpy.array
    :return: A matrix that results from multiplying m1 by m2.
    """
    return np.dot(m1, m2)

def create_perspective_projection(fovy, aspect, near, far, dtype=None):
    """Creates perspective projection matrix.

    .. seealso:: http://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml
    .. seealso:: http://www.geeks3d.com/20090729/howto-perspective-projection-matrix-in-opengl/

    :param float fovy: field of view in y direction in degrees
    :param float aspect: aspect ratio of the view (width / height)
    :param float near: distance from the viewer to the near clipping plane (only positive)
    :param float far: distance from the viewer to the far clipping plane (only positive)
    :rtype: numpy.array
    :return: A projection matrix representing the specified perpective.
    """
    ymax = near * np.tan(fovy * np.pi / 360.0)
    xmax = ymax * aspect
    return create_perspective_projection_from_bounds(-xmax, xmax, -ymax, ymax, near, far, dtype=dtype)

def create_perspective_projection_matrix(fovy, aspect, near, far, dtype=None):    # TDOO: mark as deprecated
    """Creates perspective projection matrix.

    .. seealso:: http://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml
    .. seealso:: http://www.geeks3d.com/20090729/howto-perspective-projection-matrix-in-opengl/

    :param float fovy: field of view in y direction in degrees
    :param float aspect: aspect ratio of the view (width / height)
    :param float near: distance from the viewer to the near clipping plane (only positive)
    :param float far: distance from the viewer to the far clipping plane (only positive)
    :rtype: numpy.array
    :return: A projection matrix representing the specified perpective.
    """
    return create_perspective_projection(fovy, aspect, near, far, dtype)

def create_perspective_projection_from_bounds(
    left,
    right,
    bottom,
    top,
    near,
    far,
    dtype=None
):
    """Creates a perspective projection matrix using the specified near
    plane dimensions.

    :param float left: The left of the near plane relative to the plane's centre.
    :param float right: The right of the near plane relative to the plane's centre.
    :param float top: The top of the near plane relative to the plane's centre.
    :param float bottom: The bottom of the near plane relative to the plane's centre.
    :param float near: The distance of the near plane from the camera's origin.
        It is recommended that the near plane is set to 1.0 or above to avoid rendering issues
        at close range.
    :param float far: The distance of the far plane from the camera's origin.
    :rtype: numpy.array
    :return: A projection matrix representing the specified perspective.

    .. seealso:: http://www.gamedev.net/topic/264248-building-a-projection-matrix-without-api/
    .. seealso:: http://www.glprogramming.com/red/chapter03.html
    """

    """
    E 0 A 0
    0 F B 0
    0 0 C D
    0 0-1 0

    A = (right+left)/(right-left)
    B = (top+bottom)/(top-bottom)
    C = -(far+near)/(far-near)
    D = -2*far*near/(far-near)
    E = 2*near/(right-left)
    F = 2*near/(top-bottom)
    """
    A = (right + left) / (right - left)
    B = (top + bottom) / (top - bottom)
    C = -(far + near) / (far - near)
    D = -2. * far * near / (far - near)
    E = 2. * near / (right - left)
    F = 2. * near / (top - bottom)

    return np.array((
        (  E, 0., 0., 0.),
        ( 0.,  F, 0., 0.),
        (  A,  B,  C,-1.),
        ( 0., 0.,  D, 0.),
    ), dtype=dtype)

def create_perspective_projection_matrix_from_bounds(
    left, right, bottom, top, near, far, dtype=None):    # TDOO: mark as deprecated
    """Creates a perspective projection matrix using the specified near
    plane dimensions.

    :param float left: The left of the near plane relative to the plane's centre.
    :param float right: The right of the near plane relative to the plane's centre.
    :param float top: The top of the near plane relative to the plane's centre.
    :param float bottom: The bottom of the near plane relative to the plane's centre.
    :param float near: The distance of the near plane from the camera's origin.
        It is recommended that the near plane is set to 1.0 or above to avoid rendering issues
        at close range.
    :param float far: The distance of the far plane from the camera's origin.
    :rtype: numpy.array
    :return: A projection matrix representing the specified perspective.

    .. seealso:: http://www.gamedev.net/topic/264248-building-a-projection-matrix-without-api/
    .. seealso:: http://www.glprogramming.com/red/chapter03.html
    """

    """
    E 0 A 0
    0 F B 0
    0 0 C D
    0 0-1 0

    A = (right+left)/(right-left)
    B = (top+bottom)/(top-bottom)
    C = -(far+near)/(far-near)
    D = -2*far*near/(far-near)
    E = 2*near/(right-left)
    F = 2*near/(top-bottom)
    """
    return create_perspective_projection_from_bounds(
        left, right, bottom, top, near, far, dtype
    )

def create_orthogonal_projection(
    left,
    right,
    bottom,
    top,
    near,
    far,
    dtype=None
):
    """Creates an orthogonal projection matrix.

    :param float left: The left of the near plane relative to the plane's centre.
    :param float right: The right of the near plane relative to the plane's centre.
    :param float top: The top of the near plane relative to the plane's centre.
    :param float bottom: The bottom of the near plane relative to the plane's centre.
    :param float near: The distance of the near plane from the camera's origin.
        It is recommended that the near plane is set to 1.0 or above to avoid rendering issues
        at close range.
    :param float far: The distance of the far plane from the camera's origin.
    :rtype: numpy.array
    :return: A projection matrix representing the specified orthogonal perspective.

    .. seealso:: http://msdn.microsoft.com/en-us/library/dd373965(v=vs.85).aspx
    """

    """
    A 0 0 Tx
    0 B 0 Ty
    0 0 C Tz
    0 0 0 1

    A = 2 / (right - left)
    B = 2 / (top - bottom)
    C = -2 / (far - near)

    Tx = (right + left) / (right - left)
    Ty = (top + bottom) / (top - bottom)
    Tz = (far + near) / (far - near)
    """
    rml = right - left
    tmb = top - bottom
    fmn = far - near

    A = 2. / rml
    B = 2. / tmb
    C = -2. / fmn
    Tx = -(right + left) / rml
    Ty = -(top + bottom) / tmb
    Tz = -(far + near) / fmn

    return np.array((
        ( A, 0., 0., 0.),
        (0.,  B, 0., 0.),
        (0., 0.,  C, 0.),
        (Tx, Ty, Tz, 1.),
    ), dtype=dtype)

def create_orthogonal_projection_matrix(
    left, right, bottom, top, near, far, dtype=None):    # TDOO: mark as deprecated
    """Creates an orthogonal projection matrix.

    :param float left: The left of the near plane relative to the plane's centre.
    :param float right: The right of the near plane relative to the plane's centre.
    :param float top: The top of the near plane relative to the plane's centre.
    :param float bottom: The bottom of the near plane relative to the plane's centre.
    :param float near: The distance of the near plane from the camera's origin.
        It is recommended that the near plane is set to 1.0 or above to avoid rendering issues
        at close range.
    :param float far: The distance of the far plane from the camera's origin.
    :rtype: numpy.array
    :return: A projection matrix representing the specified orthogonal perspective.

    .. seealso:: http://msdn.microsoft.com/en-us/library/dd373965(v=vs.85).aspx
    """

    """
    A 0 0 Tx
    0 B 0 Ty
    0 0 C Tz
    0 0 0 1

    A = 2 / (right - left)
    B = 2 / (top - bottom)
    C = -2 / (far - near)

    Tx = (right + left) / (right - left)
    Ty = (top + bottom) / (top - bottom)
    Tz = (far + near) / (far - near)
    """
    return create_orthogonal_projection(
        left, right, bottom, top, near, far, dtype
    )

def create_look_at(eye, target, up, dtype=None):
    """Creates a look at matrix according to OpenGL standards.

    :param numpy.array eye: Position of the camera in world coordinates.
    :param numpy.array target: The position in world coordinates that the
        camera is looking at.
    :param numpy.array up: The up vector of the camera.
    :rtype: numpy.array
    :return: A look at matrix that can be used as a viewMatrix
    """

    eye = np.asarray(eye)
    target = np.asarray(target)
    up = np.asarray(up)

    forward = vector.normalize(target - eye)
    side = vector.normalize(np.cross(forward, up))
    up = vector.normalize(np.cross(side, forward))

    return np.array((
            (side[0], up[0], -forward[0], 0.),
            (side[1], up[1], -forward[1], 0.),
            (side[2], up[2], -forward[2], 0.),
            (-np.dot(side, eye), -np.dot(up, eye), np.dot(forward, eye), 1.0)
        ), dtype=dtype)


def inverse(m):
    """Returns the inverse of the matrix.

    This is essentially a wrapper around numpy.linalg.inv.

    :param numpy.array m: A matrix.
    :rtype: numpy.array
    :return: The inverse of the specified matrix.

    .. seealso:: http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.inv.html
    """
    return np.linalg.inv(m)

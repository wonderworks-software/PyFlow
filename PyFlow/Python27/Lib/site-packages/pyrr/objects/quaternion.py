# -*- coding: utf-8 -*-
"""Represents a Quaternion rotation.

The Quaternion class provides a number of convenient functions and
conversions.
::

    import numpy as np
    from pyrr import Quaternion, Matrix33, Matrix44, Vector3, Vector4

    q = Quaternion()

    # explicit creation
    q = Quaternion.from_x_rotation(np.pi / 2.0)
    q = Quaternion.from_matrix(Matrix33.identity())
    q = Quaternion.from_matrix(Matrix44.identity())

    # inferred conversions
    q = Quaternion(Quaternion())
    q = Quaternion(Matrix33.identity())
    q = Quaternion(Matrix44.identity())

    # apply one quaternion to another
    q1 = Quaternion.from_y_rotation(np.pi / 2.0)
    q2 = Quaternion.from_x_rotation(np.pi / 2.0)
    q3 = q1 * q2

    # extract a matrix from the quaternion
    m33 = q3.matrix33
    m44 = q3.matrix44

    # convert from matrix back to quaternion
    q4 = Quaternion(m44)

    # rotate a quaternion by a matrix
    q = Quaternion() * Matrix33.identity()
    q = Quaternion() * Matrix44.identity()

    # apply quaternion to a vector
    v3 = Quaternion() * Vector3()
    v4 = Quaternion() * Vector4()

    # undo a rotation
    q = Quaternion.from_x_rotation(np.pi / 2.0)
    v = q * Vector3([1.,1.,1.])
    # ~q is the same as q.conjugate
    original = ~q * v
    assert np.allclose(original, v)

    # get the dot product of 2 Quaternions
    dot = Quaternion() | Quaternion.from_x_rotation(np.pi / 2.0)
"""

from __future__ import absolute_import
import numpy as np
from multipledispatch import dispatch
from .base import BaseObject, BaseQuaternion, BaseMatrix, BaseVector, NpProxy
from .. import quaternion

class Quaternion(BaseQuaternion):
    _module = quaternion
    _shape = (4,)

    #: The X value of this Quaternion.
    x = NpProxy(0)
    #: The Y value of this Quaternion.
    y = NpProxy(1)
    #: The Z value of this Quaternion.
    z = NpProxy(2)
    #: The W value of this Quaternion.
    w = NpProxy(3)
    #: The X,Y value of this Quaternion as a numpy.ndarray.
    xy = NpProxy([0,1])
    #: The X,Y,Z value of this Quaternion as a numpy.ndarray.
    xyz = NpProxy([0,1,2])
    #: The X,Y,Z,W value of this Quaternion as a numpy.ndarray.
    xyzw = NpProxy([0,1,2,3])
    #: The X,Z value of this Quaternion as a numpy.ndarray.
    xz = NpProxy([0,2])
    #: The X,Z,W value of this Quaternion as a numpy.ndarray.
    xzw = NpProxy([0,2,3])
    #: The X,Y,W value of this Quaternion as a numpy.ndarray.
    xyw = NpProxy([0,1,3])
    #: The X,W value of this Quaternion as a numpy.ndarray.
    xw = NpProxy([0,3])

    ########################
    # Creation
    @classmethod
    def from_x_rotation(cls, theta, dtype=None):
        """Creates a new Quaternion with a rotation around the X-axis.
        """
        return cls(quaternion.create_from_x_rotation(theta, dtype))

    @classmethod
    def from_y_rotation(cls, theta, dtype=None):
        """Creates a new Quaternion with a rotation around the Y-axis.
        """
        return cls(quaternion.create_from_y_rotation(theta, dtype))

    @classmethod
    def from_z_rotation(cls, theta, dtype=None):
        """Creates a new Quaternion with a rotation around the Z-axis.
        """
        return cls(quaternion.create_from_z_rotation(theta, dtype))

    @classmethod
    def from_axis_rotation(cls, axis, theta, dtype=None):
        """Creates a new Quaternion with a rotation around the specified axis.
        """
        return cls(quaternion.create_from_axis_rotation(axis, theta, dtype))

    @classmethod
    def from_matrix(cls, matrix, dtype=None):
        """Creates a Quaternion from the specified Matrix (Matrix33 or Matrix44).
        """
        return cls(quaternion.create_from_matrix(matrix, dtype))

    @classmethod
    def from_eulers(cls, eulers, dtype=None):
        """Creates a Quaternion from the specified Euler angles.
        """
        return cls(quaternion.create_from_eulers(eulers, dtype))

    @classmethod
    def from_inverse_of_eulers(cls, eulers, dtype=None):
        """Creates a Quaternion from the inverse of the specified Euler angles.
        """
        return cls(quaternion.create_from_inverse_of_eulers(eulers, dtype))

    def __new__(cls, value=None, dtype=None):
        if value is not None:
            obj = value
            if not isinstance(value, np.ndarray):
                obj = np.array(value, dtype=dtype)

            # matrix33, matrix44
            if obj.shape in ((4,4,), (3,3,)) or isinstance(obj, (Matrix33, Matrix44)):
                obj = quaternion.create_from_matrix(obj, dtype=dtype)
        else:
            obj = quaternion.create(dtype=dtype)
        obj = obj.view(cls)
        return super(Quaternion, cls).__new__(cls, obj)

    ########################
    # Basic Operators
    @dispatch(BaseObject)
    def __add__(self, other):
        self._unsupported_type('add', other)

    @dispatch(BaseObject)
    def __sub__(self, other):
        self._unsupported_type('subtract', other)

    @dispatch(BaseObject)
    def __mul__(self, other):
        self._unsupported_type('multiply', other)

    @dispatch(BaseObject)
    def __truediv__(self, other):
        self._unsupported_type('divide', other)

    @dispatch(BaseObject)
    def __div__(self, other):
        self._unsupported_type('divide', other)

    ########################
    # Quaternions
    @dispatch((BaseQuaternion, np.ndarray, list))
    def __sub__(self, other):
        return Quaternion(super(Quaternion, self).__sub__(other))

    @dispatch((BaseQuaternion, list))
    def __mul__(self, other):
        return self.cross(other)

    @dispatch((BaseQuaternion, list))
    def __or__(self, other):
        return self.dot(other)

    def __invert__(self):
        return self.conjugate

    ########################
    # Matrices
    @dispatch(BaseMatrix)
    def __mul__(self, other):
        return self * Quaternion(other)

    ########################
    # Vectors
    @dispatch(BaseVector)
    def __mul__(self, other):
        return type(other)(quaternion.apply_to_vector(self, other))

    ########################
    # Methods and Properties
    @property
    def length(self):
        """Returns the length of this Quaternion.
        """
        return quaternion.length(self)

    def normalize(self):
        """normalizes this Quaternion in-place.
        """
        self[:] = quaternion.normalize(self)

    @property
    def normalized(self):
        """Returns a normalized version of this Quaternion as a new Quaternion.
        """
        return Quaternion(quaternion.normalize(self))

    def normalise(self):    # TODO: mark as deprecated
        """normalizes this Quaternion in-place.
        """
        self[:] = quaternion.normalize(self)

    @property
    def normalised(self):    # TODO: mark as deprecated
        """Returns a normalized version of this Quaternion as a new Quaternion.
        """
        return Quaternion(quaternion.normalize(self))

    @property
    def angle(self):
        """Returns the angle around the axis of rotation of this Quaternion as a float.
        """
        return quaternion.rotation_angle(self)

    @property
    def axis(self):
        """Returns the axis of rotation of this Quaternion as a Vector3.
        """
        return Vector3(quaternion.rotation_axis(self))

    def cross(self, other):
        """Returns the cross of this Quaternion and another.

        This is the equivalent of combining Quaternion rotations (like Matrix multiplication).
        """
        return Quaternion(quaternion.cross(self, other))

    def lerp(self, other, t):
        """Interpolates between quat1 and quat2 by t.
        The parameter t is clamped to the range [0, 1]
        """
        return Quaternion(quaternion.lerp(self, other, t))

    def slerp(self, other, t):
        """Spherically interpolates between quat1 and quat2 by t.
        The parameter t is clamped to the range [0, 1]
        """
        return Quaternion(quaternion.slerp(self, other, t))

    def dot(self, other):
        """Returns the dot of this Quaternion and another.
        """
        return quaternion.dot(self, other)

    @property
    def conjugate(self):
        """Returns the conjugate of this Quaternion.

        This is a Quaternion with the opposite rotation.
        """
        return Quaternion(quaternion.conjugate(self))

    @property
    def inverse(self):
        """Returns the inverse of this quaternion.
        """
        return Quaternion(quaternion.inverse(self))

    def power(self, exponent):
        """Returns a new Quaternion representing this Quaternion to the power of the exponent.
        """
        return Quaternion(quaternion.power(self, exponent))

    @property
    def negative(self):
        """Returns the negative of the Quaternion.
        """
        return Quaternion(quaternion.negate(self))

    @property
    def is_identity(self):
        """Returns True if the Quaternion has no rotation (0.,0.,0.,1.).
        """
        return quaternion.is_identity(self)

    @property
    def matrix44(self):
        """Returns a Matrix44 representation of this Quaternion.
        """
        return Matrix44.from_quaternion(self)

    @property
    def matrix33(self):
        """Returns a Matrix33 representation of this Quaternion.
        """
        return Matrix33.from_quaternion(self)

from .vector3 import Vector3
from .matrix33 import Matrix33
from .matrix44 import Matrix44

# -*- coding: utf-8 -*-
"""Represents a 4x4 Matrix.

The Matrix44 class provides a number of convenient functions and
conversions.
::

    import numpy as np
    from pyrr import Quaternion, Matrix33, Matrix44, Vector4

    m = Matrix44()
    m = Matrix44([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]])

    # copy constructor
    m = Matrix44(Matrix44())

    # explicit creation
    m = Matrix44.identity()
    m = Matrix44.from_matrix44(Matrix44())

    # inferred conversions
    m = Matrix44(Quaternion())
    m = Matrix44(Matrix33())

    # multiply matricies together
    m = Matrix44() * Matrix44()

    # extract a quaternion from a matrix
    q = m.quaternion

    # convert from quaternion back to matrix
    m = q.matrix44
    m = Matrix44(q)

    # rotate a matrix by a quaternion
    m = Matrix44.identity() * Quaternion()

    # rotate a vector 4 by a matrix
    v = Matrix44.from_x_rotation(np.pi) * Vector4([1.,2.,3.,1.])

    # undo a rotation
    m = Matrix44.from_x_rotation(np.pi)
    v = m * Vector4([1.,1.,1.,1.])
    # ~m is the same as m.inverse
    v = ~m * v

    # access specific parts of the matrix
    # first row
    m1 = m.m1
    # first element, first row
    m11 = m.m11
    # fourth element, fourth row
    m44 = m.m44
    # first row, same as m1
    r1 = m.r1
    # first column
    c1 = m.c1
"""
from __future__ import absolute_import
from numbers import Number
import numpy as np
from multipledispatch import dispatch
from .base import BaseObject, BaseMatrix, BaseMatrix44, BaseQuaternion, BaseVector, NpProxy
from .. import matrix44

class Matrix44(BaseMatrix44):
    _module = matrix44
    _shape = (4,4,)

    # m<c> style access
    #: The first row of this Matrix as a numpy.ndarray.
    m1 = NpProxy(0)
    #: The second row of this Matrix as a numpy.ndarray.
    m2 = NpProxy(1)
    #: The third row of this Matrix as a numpy.ndarray.
    m3 = NpProxy(2)
    #: The fourth row of this Matrix as a numpy.ndarray.
    m4 = NpProxy(3)

    # m<r><c> access
    #: The [0,0] value of this Matrix.
    m11 = NpProxy((0,0))
    #: The [0,1] value of this Matrix.
    m12 = NpProxy((0,1))
    #: The [0,2] value of this Matrix.
    m13 = NpProxy((0,2))
    #: The [0,3] value of this Matrix.
    m14 = NpProxy((0,3))
    #: The [1,0] value of this Matrix.
    m21 = NpProxy((1,0))
    #: The [1,1] value of this Matrix.
    m22 = NpProxy((1,1))
    #: The [1,2] value of this Matrix.
    m23 = NpProxy((1,2))
    #: The [1,3] value of this Matrix.
    m24 = NpProxy((1,3))
    #: The [2,0] value of this Matrix.
    m31 = NpProxy((2,0))
    #: The [2,1] value of this Matrix.
    m32 = NpProxy((2,1))
    #: The [2,2] value of this Matrix.
    m33 = NpProxy((2,2))
    #: The [2,3] value of this Matrix.
    m34 = NpProxy((2,3))
    #: The [3,0] value of this Matrix.
    m41 = NpProxy((3,0))
    #: The [3,1] value of this Matrix.
    m42 = NpProxy((3,1))
    #: The [3,2] value of this Matrix.
    m43 = NpProxy((3,2))
    #: The [3,3] value of this Matrix.
    m44 = NpProxy((3,3))

    # rows
    #: The first row of this Matrix as a numpy.ndarray. This is the same as m1.
    r1 = NpProxy(0)
    #: The second row of this Matrix as a numpy.ndarray. This is the same as m2.
    r2 = NpProxy(1)
    #: The third row of this Matrix as a numpy.ndarray. This is the same as m3.
    r3 = NpProxy(2)
    #: The fourth row of this Matrix as a numpy.ndarray. This is the same as m4.
    r4 = NpProxy(3)

    # columns
    #: The first column of this Matrix as a numpy.ndarray.
    c1 = NpProxy((slice(0,4),0))
    #: The second column of this Matrix as a numpy.ndarray.
    c2 = NpProxy((slice(0,4),1))
    #: The third column of this Matrix as a numpy.ndarray.
    c3 = NpProxy((slice(0,4),2))
    #: The fourth column of this Matrix as a numpy.ndarray.
    c4 = NpProxy((slice(0,4),3))

    ########################
    # Creation
    @classmethod
    def from_matrix33(cls, matrix, dtype=None):
        """Creates a Matrix44 from a Matrix33.
        """
        return cls(matrix44.create_from_matrix33(matrix, dtype))

    @classmethod
    def perspective_projection(cls, fovy, aspect, near, far, dtype=None):
        """Creates a Matrix44 for use as a perspective projection matrix.
        """
        return cls(matrix44.create_perspective_projection(fovy, aspect, near, far, dtype))

    @classmethod
    def perspective_projection_bounds(cls, left, right, top, bottom, near, far, dtype=None):
        """Creates a Matrix44 for use as a perspective projection matrix.
        """
        return cls(matrix44.create_perspective_projection_from_bounds(left, right, top, bottom, near, far, dtype))

    @classmethod
    def orthogonal_projection(cls, left, right, top, bottom, near, far, dtype=None):
        """Creates a Matrix44 for use as an orthogonal projection matrix.
        """
        return cls(matrix44.create_orthogonal_projection(left, right, top, bottom, near, far, dtype))

    @classmethod
    def look_at(cls, eye, target, up, dtype=None):
        """Creates a Matrix44 for use as a lookAt matrix.
        """
        return cls(matrix44.create_look_at(eye, target, up, dtype))

    @classmethod
    def from_translation(cls, translation, dtype=None):
        """Creates a Matrix44 from the specified translation.
        """
        return cls(matrix44.create_from_translation(translation, dtype=dtype))

    def __new__(cls, value=None, dtype=None):
        if value is not None:
            obj = value
            if not isinstance(value, np.ndarray):
                obj = np.array(value, dtype=dtype)

            # matrix33
            if obj.shape == (3,3) or isinstance(obj, Matrix33):
                obj = matrix44.create_from_matrix33(obj, dtype=dtype)
            # quaternion
            elif obj.shape == (4,) or isinstance(obj, Quaternion):
                obj = matrix44.create_from_quaternion(obj, dtype=dtype)
        else:
            obj = np.zeros(cls._shape, dtype=dtype)
        obj = obj.view(cls)
        return super(Matrix44, cls).__new__(cls, obj)

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

    def __invert__(self):
        return self.inverse

    ########################
    # Matrices
    @dispatch((BaseMatrix, np.ndarray, list))
    def __add__(self, other):
        return Matrix44(super(Matrix44, self).__add__(Matrix44(other)))

    @dispatch((BaseMatrix, np.ndarray, list))
    def __sub__(self, other):
        return Matrix44(super(Matrix44, self).__sub__(Matrix44(other)))

    @dispatch((BaseMatrix, np.ndarray, list))
    def __mul__(self, other):
        return Matrix44(matrix44.multiply(Matrix44(other), self))

    ########################
    # Quaternions
    @dispatch(BaseQuaternion)
    def __mul__(self, other):
        m = other.matrix44
        return self * m

    ########################
    # Vectors
    @dispatch(BaseVector)
    def __mul__(self, other):
        return type(other)(matrix44.apply_to_vector(self, other))

    ########################
    # Number
    @dispatch((Number, np.number))
    def __add__(self, other):
        return Matrix44(super(Matrix44, self).__add__(other))

    @dispatch((Number, np.number))
    def __sub__(self, other):
        return Matrix44(super(Matrix44, self).__sub__(other))

    @dispatch((Number, np.number))
    def __mul__(self, other):
        return Matrix44(super(Matrix44, self).__mul__(other))

    @dispatch((Number, np.number))
    def __truediv__(self, other):
        return Matrix44(super(Matrix44, self).__truediv__(other))

    @dispatch((Number, np.number))
    def __div__(self, other):
        return Matrix44(super(Matrix44, self).__div__(other))

    ########################
    # Methods and Properties
    @property
    def matrix33(self):
        """Returns a Matrix33 representing this matrix.
        """
        return Matrix33(self)

    @property
    def matrix44(self):
        """Returns the Matrix44.

        This can be handy if you're not sure what type of Matrix class you have
        but require a Matrix44.
        """
        return self

    @property
    def quaternion(self):
        """Returns a Quaternion representing this matrix.
        """
        return Quaternion(self)

from .matrix33 import Matrix33
from .quaternion import Quaternion

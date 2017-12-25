# -*- coding: utf-8 -*-
"""Represents a 3x3 Matrix.

The Matrix33 class provides a number of convenient functions and
conversions.
::

    import numpy as np
    from pyrr import Quaternion, Matrix33, Matrix44, Vector3

    m = Matrix33()
    m = Matrix33([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])

    # copy constructor
    m = Matrix44(Matrix44())

    # explicit creation
    m = Matrix33.identity()
    m = Matrix33.from_matrix44(Matrix44())

    # inferred conversions
    m = Matrix33(Quaternion())
    m = Matrix33(Matrix44())

    # multiply matricies together
    m = Matrix33() * Matrix33()
    m = Matrix33() * Matrix44()

    # extract a quaternion from a matrix
    q = m.quaternion

    # convert from quaternion back to matrix
    m = q.matrix33
    m = Matrix33(q)

    # rotate a matrix by a quaternion
    m = Matrix33.identity() * Quaternion()

    # rotate a vector 3 by a matrix
    v = Matrix33.from_x_rotation(np.pi) * Vector3([1.,2.,3.])

    # undo a rotation
    m = Matrix33.from_x_rotation(np.pi)
    v = m * Vector3([1.,1.,1.])
    # ~m is the same as m.inverse
    v = ~m * v

    # access specific parts of the matrix
    # first row
    m1 = m.m1
    # first element, first row
    m11 = m.m11
    # third element, third row
    m33 = m.m33
    # first row, same as m1
    r1 = m.r1
    # first column
    c1 = m.c1
"""
from __future__ import absolute_import
from numbers import Number
import numpy as np
from multipledispatch import dispatch
from .base import BaseObject, BaseMatrix, BaseMatrix33, BaseQuaternion, BaseVector, NpProxy
from .. import matrix33

class Matrix33(BaseMatrix33):
    _module = matrix33
    _shape = (3,3,)

    # m<c> style access
    #: The first row of this Matrix as a numpy.ndarray.
    m1 = NpProxy(0)
    #: The second row of this Matrix as a numpy.ndarray.
    m2 = NpProxy(1)
    #: The third row of this Matrix as a numpy.ndarray.
    m3 = NpProxy(2)

    # m<r><c> access
    #: The [0,0] value of this Matrix.
    m11 = NpProxy((0,0))
    #: The [0,1] value of this Matrix.
    m12 = NpProxy((0,1))
    #: The [0,2] value of this Matrix.
    m13 = NpProxy((0,2))
    #: The [1,0] value of this Matrix.
    m21 = NpProxy((1,0))
    #: The [1,1] value of this Matrix.
    m22 = NpProxy((1,1))
    #: The [1,2] value of this Matrix.
    m23 = NpProxy((1,2))
    #: The [2,0] value of this Matrix.
    m31 = NpProxy((2,0))
    #: The [2,1] value of this Matrix.
    m32 = NpProxy((2,1))
    #: The [2,2] value of this Matrix.
    m33 = NpProxy((2,2))

    # rows
    #: The first row of this Matrix as a numpy.ndarray. This is the same as m1.
    r1 = NpProxy(0)
    #: The second row of this Matrix as a numpy.ndarray. This is the same as m2.
    r2 = NpProxy(1)
    #: The third row of this Matrix as a numpy.ndarray. This is the same as m3.
    r3 = NpProxy(2)

    # columns
    #: The first column of this Matrix as a numpy.ndarray.
    c1 = NpProxy((slice(0,3),0))
    #: The second column of this Matrix as a numpy.ndarray.
    c2 = NpProxy((slice(0,3),1))
    #: The third column of this Matrix as a numpy.ndarray.
    c3 = NpProxy((slice(0,3),2))

    ########################
    # Creation
    @classmethod
    def from_matrix44(cls, matrix, dtype=None):
        """Creates a Matrix33 from a Matrix44.

        The Matrix44 translation will be lost.
        """
        return cls(matrix33.create_from_matrix44(matrix, dtype))

    def __new__(cls, value=None, dtype=None):
        if value is not None:
            obj = value
            if not isinstance(value, np.ndarray):
                obj = np.array(value, dtype=dtype)

            # matrix44
            if obj.shape == (4,4) or isinstance(obj, Matrix44):
                obj = matrix33.create_from_matrix44(obj, dtype=dtype)
            # quaternion
            elif obj.shape == (4,) or isinstance(obj, Quaternion):
                obj = matrix33.create_from_quaternion(obj, dtype=dtype)
        else:
            obj = np.zeros(cls._shape, dtype=dtype)
        obj = obj.view(cls)
        return super(Matrix33, cls).__new__(cls, obj)

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
        return Matrix33(super(Matrix33, self).__add__(Matrix33(other)))

    @dispatch((BaseMatrix, np.ndarray, list))
    def __sub__(self, other):
        return Matrix33(super(Matrix33, self).__sub__(Matrix33(other)))

    @dispatch((BaseMatrix, np.ndarray, list))
    def __mul__(self, other):
        return Matrix33(matrix33.multiply(Matrix33(other), self))

    ########################
    # Quaternions
    @dispatch(BaseQuaternion)
    def __mul__(self, other):
        m = other.matrix33
        return self * m

    ########################
    # Vectors
    @dispatch(BaseVector)
    def __mul__(self, other):
        return type(other)(matrix33.apply_to_vector(self, other))

    ########################
    # Number
    @dispatch((Number, np.number))
    def __add__(self, other):
        return Matrix33(super(Matrix33, self).__add__(other))

    @dispatch((Number, np.number))
    def __sub__(self, other):
        return Matrix33(super(Matrix33, self).__sub__(other))

    @dispatch((Number, np.number))
    def __mul__(self, other):
        return Matrix33(super(Matrix33, self).__mul__(other))

    @dispatch((Number, np.number))
    def __truediv__(self, other):
        return Matrix33(super(Matrix33, self).__truediv__(other))

    @dispatch((Number, np.number))
    def __div__(self, other):
        return Matrix33(super(Matrix33, self).__div__(other))

    ########################
    # Methods and Properties
    @property
    def matrix33(self):
        """Returns the Matrix33.

        This can be handy if you're not sure what type of Matrix class you have
        but require a Matrix33.
        """
        return self

    @property
    def matrix44(self):
        """Returns a Matrix44 representing this matrix.
        """
        return Matrix44(self)

    @property
    def quaternion(self):
        """Returns a Quaternion representing this matrix.
        """
        return Quaternion(self)

from .matrix44 import Matrix44
from .quaternion import Quaternion

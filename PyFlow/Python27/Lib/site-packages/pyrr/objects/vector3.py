# -*- coding: utf-8 -*-
"""Represents a 3 dimensional Vector.

The Vector3 class provides a number of convenient functions and
conversions.
::

    import numpy as np
    from pyrr import Quaternion, Matrix33, Matrix44, Vector3

    v = Vector3()
    v = Vector3([1.,2.,3.])

    # copy constructor
    v = Vector3(Vector3())

    # add / subtract vectors
    v = Vector3([1.,2.,3.]) + Vector3([4.,5.,6.])

    # rotate a vector by a Matrix
    v = Matrix33.identity() * Vector3([1.,2.,3.])
    v = Matrix44.identity() * Vector3([1.,2.,3.])

    # rotate a vector by a Quaternion
    v = Quaternion() * Vector3([1.,2.,3.])

    # get the dot-product of 2 vectors
    d = Vector3([1.,0.,0.]) | Vector3([0.,1.,0.])

    # get the cross-product of 2 vectors
    x = Vector3([1.,0.,0.]) ^ Vector3([0.,1.,0.])

    # access specific parts of the vector
    # x value
    x,y,z = v.x, v.y, v.z

    # access groups of values as np.ndarray's
    xy = v.xy
    xz = v.xz
    xyz = v.xyz
"""
from __future__ import absolute_import, division
from numbers import Number
import numpy as np
from multipledispatch import dispatch
from .base import BaseObject, BaseVector3, BaseMatrix44, NpProxy
from .. import vector3

# TODO: add < <= > >= == != operators

class Vector3(BaseVector3):
    _module = vector3
    _shape = (3,)

    #: The X value of this Vector.
    x = NpProxy(0)
    #: The Y value of this Vector.
    y = NpProxy(1)
    #: The Z value of this Vector.
    z = NpProxy(2)
    #: The X,Y values of this Vector as a numpy.ndarray.
    xy = NpProxy([0,1])
    #: The X,Y,Z values of this Vector as a numpy.ndarray.
    xyz = NpProxy([0,1,2])
    #: The X,Z values of this Vector as a numpy.ndarray.
    xz = NpProxy([0,2])

    ########################
    # Creation
    @classmethod
    def from_vector4(cls, vector, dtype=None):
        """Create a Vector3 from a Vector4.

        Returns the Vector3 and the W component as a tuple.
        """
        vec, w = vector3.create_from_vector4(vector, dtype)
        return (cls(vec), w)

    def __new__(cls, value=None, w=0.0, dtype=None):
        if value is not None:
            obj = value
            if not isinstance(value, np.ndarray):
                obj = np.array(value, dtype=dtype)

            # matrix44
            if obj.shape in ((4,4,)) or isinstance(obj, BaseMatrix44):
                obj = vector3.create_from_matrix44_translation(obj, dtype=dtype)
        else:
            obj = np.zeros(cls._shape, dtype=dtype)
        obj = obj.view(cls)
        return super(Vector3, cls).__new__(cls, obj)

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

    @dispatch((BaseObject, Number, np.number))
    def __xor__(self, other):
        self._unsupported_type('XOR', other)

    @dispatch((BaseObject, Number, np.number))
    def __or__(self, other):
        self._unsupported_type('OR', other)

    @dispatch((BaseObject, Number, np.number))
    def __ne__(self, other):
        self._unsupported_type('NE', other)

    @dispatch((BaseObject, Number, np.number))
    def __eq__(self, other):
        self._unsupported_type('EQ', other)

    ########################
    # Vectors
    @dispatch((BaseVector3, np.ndarray, list))
    def __add__(self, other):
        return Vector3(super(Vector3, self).__add__(other))

    @dispatch((BaseVector3, np.ndarray, list))
    def __sub__(self, other):
        return Vector3(super(Vector3, self).__sub__(other))

    @dispatch((BaseVector3, np.ndarray, list))
    def __mul__(self, other):
        return Vector3(super(Vector3, self).__mul__(other))

    @dispatch((BaseVector3, np.ndarray, list))
    def __truediv__(self, other):
        return Vector3(super(Vector3, self).__truediv__(other))

    @dispatch((BaseVector3, np.ndarray, list))
    def __div__(self, other):
        return Vector3(super(Vector3, self).__div__(other))

    @dispatch((BaseVector3, np.ndarray, list))
    def __xor__(self, other):
        return self.cross(other)

    @dispatch((BaseVector3, np.ndarray, list))
    def __or__(self, other):
        return self.dot(other)

    @dispatch((BaseVector3, np.ndarray, list))
    def __ne__(self, other):
        return bool(np.any(super(Vector3, self).__ne__(other)))

    @dispatch((BaseVector3, np.ndarray, list))
    def __eq__(self, other):
        return bool(np.all(super(Vector3, self).__eq__(other)))

    ########################
    # Number
    @dispatch((Number,np.number))
    def __add__(self, other):
        return Vector3(super(Vector3, self).__add__(other))

    @dispatch((Number,np.number))
    def __sub__(self, other):
        return Vector3(super(Vector3, self).__sub__(other))

    @dispatch((Number,np.number))
    def __mul__(self, other):
        return Vector3(super(Vector3, self).__mul__(other))

    @dispatch((Number,np.number))
    def __truediv__(self, other):
        return Vector3(super(Vector3, self).__truediv__(other))

    @dispatch((Number,np.number))
    def __div__(self, other):
        return Vector3(super(Vector3, self).__div__(other))

    ########################
    # Methods and Properties
    @property
    def inverse(self):
        """Returns the opposite of this vector.
        """
        return Vector3(-self)

    @property
    def vector3(self):
        return self

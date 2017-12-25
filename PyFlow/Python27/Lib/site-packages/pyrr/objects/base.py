# -*- coding: utf-8 -*-
from __future__ import absolute_import
import numpy as np
from pyrr import vector, vector3

class NpProxy(object):
    def __init__(self, index):
        self._index = index

    def __get__(self, obj, cls):
        return obj[self._index]

    def __set__(self, obj, value):
        obj[self._index] = value

class BaseObject(np.ndarray):
    _module = None
    _shape = None
    def __new__(cls, obj):
        # ensure the object matches the required shape
        obj.shape = cls._shape
        return obj

    def _unsupported_type(self, method, other):
        raise ValueError('Cannot {} a {} to a {}'.format(method, type(other).__name__, type(self).__name__))

    ########################
    # Redirect assignment operators
    def __iadd__(self, other):
        self[:] = self.__add__(other)
        return self

    def __isub__(self, other):
        self[:] = self.__sub__(other)
        return self

    def __imul__(self, other):
        self[:] = self.__mul__(other)
        return self

    def __idiv__(self, other):
        self[:] = self.__div__(other)
        return self

class BaseMatrix(BaseObject):
    @classmethod
    def identity(cls, dtype=None):
        """Creates an identity Matrix.
        """
        return cls(cls._module.create_identity(dtype), dtype)

    @classmethod
    def from_eulers(cls, eulers, dtype=None):
        """Creates a Matrix from the specified Euler angles.
        """
        return cls(cls._module.create_from_eulers(eulers, dtype=dtype))

    @classmethod
    def from_quaternion(cls, quat, dtype=None):
        """Creates a Matrix from a Quaternion.
        """
        return cls(cls._module.create_from_quaternion(quat, dtype=dtype))

    @classmethod
    def from_inverse_of_quaternion(cls, quat, dtype=None):
        """Creates a Matrix from the inverse of the specified Quaternion.
        """
        return cls(cls._module.create_from_inverse_of_quaternion(quat, dtype=dtype))

    @classmethod
    def from_scale(cls, scale, dtype=None):
        return cls(cls._module.create_from_scale(scale, dtype=dtype))

    @classmethod
    def from_x_rotation(cls, theta, dtype=None):
        """Creates a Matrix with a rotation around the X-axis.
        """
        return cls(cls._module.create_from_x_rotation(theta, dtype=dtype))

    @classmethod
    def from_y_rotation(cls, theta, dtype=None):
        return cls(cls._module.create_from_y_rotation(theta, dtype=dtype))

    @classmethod
    def from_z_rotation(cls, theta, dtype=None):
        """Creates a Matrix with a rotation around the Z-axis.
        """
        return cls(cls._module.create_from_z_rotation(theta, dtype=dtype))

    @property
    def inverse(self):
        """Returns the inverse of this matrix.
        """
        return type(self)(self._module.inverse(self))

class BaseVector(BaseObject):
    @classmethod
    def from_matrix44_translation(cls, matrix, dtype=None):
        return cls(cls._module.create_from_matrix44_translation(matrix, dtype))

    def normalize(self):
        self[:] = self.normalized

    @property
    def normalized(self):
        return type(self)(self._module.normalize(self))

    def normalise(self):    # TODO: mark as deprecated
        self[:] = self.normalized

    @property
    def normalised(self):    # TODO: mark as deprecated
        return type(self)(self._module.normalize(self))

    @property
    def squared_length(self):
        return self._module.squared_length(self)

    @property
    def length(self):
        return self._module.length(self)

    @length.setter
    def length(self, length):
        self[:] = vector.set_length(self, length)

    def dot(self, other):
        return vector.dot(self, type(self)(other))

    def cross(self, other):
        return type(self)(vector3.cross(self[:3], other[:3]))

    def interpolate(self, other, delta):
        return type(self)(vector.interpolate(self, type(self)(other), delta))

    def normal(self, v2, v3, normalize_result=True):
        return type(self)(vector3.generate_normals(self, type(self)(v2), type(self)(v3), normalize_result))

class BaseQuaternion(BaseObject):
    pass

# pre-declarations to prevent circular imports
class BaseMatrix33(BaseMatrix):
    pass

class BaseMatrix44(BaseMatrix):
    pass

class BaseVector3(BaseVector):
    pass

class BaseVector4(BaseVector):
    pass

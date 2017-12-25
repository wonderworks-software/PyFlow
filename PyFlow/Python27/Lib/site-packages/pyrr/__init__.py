# -*- coding: utf-8 -*-
from __future__ import absolute_import

# the version of software
# this is used by the setup.py script
from .version import __version__

__all__ = [
    'aabb',
    'aambb',
    'euler',
    'geometric_tests',
    'geometry',
    'integer',
    'line',
    'matrix33',
    'matrix44',
    'plane',
    'quaternion',
    'ray',
    'rectangle',
    'sphere',
    'trig',
    'utils',
    'vector',
    'vector3',
    'vector4',
    'Matrix33',
    'Matrix44',
    'Quaternion',
    'Vector3',
    'Vector4',
]

from . import (
    aabb,
    aambb,
    euler,
    geometric_tests,
    geometry,
    integer,
    line,
    matrix33,
    matrix44,
    plane,
    quaternion,
    ray,
    rectangle,
    sphere,
    trig,
    utils,
    vector,
    vector3,
    vector4,
)

from .objects import (
    Matrix33,
    Matrix44,
    Quaternion,
    Vector3,
    Vector4
)

# because of circular imports, we cannot put these inside each module
# so insert them here
setattr(matrix33, 'Matrix33', Matrix33)
setattr(matrix44, 'Matrix44', Matrix44)
setattr(quaternion, 'Quaternion', Quaternion)
setattr(vector3, 'Vector3', Vector3)
setattr(vector4, 'Vector4', Vector4)


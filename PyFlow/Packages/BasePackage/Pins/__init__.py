"""@package Pins
"""
# from __future__ import absolute_import

# __all__ = [
#     "BoolPin",
#     "EnumPin",
#     "ExecPin",
#     "FloatPin",
#     "FloatVector3Pin",
#     "FloatVector4Pin",
#     "IntPin",
#     "ListPin",
#     "Matrix33Pin",
#     "Matrix44Pin",
#     "QuatPin",
#     "StringPin",
#     "PinUtils"
# ]

# from . import(
#     BoolPin,
#     EnumPin,
#     ExecPin,
#     FloatPin,
#     FloatVector3Pin,
#     FloatVector4Pin,
#     IntPin,
#     ListPin,
#     Matrix33Pin,
#     Matrix44Pin,
#     QuatPin,
#     StringPin,
#     PinUtils
# )


# from .BoolPin import BoolPin
# from .EnumPin import EnumPin
# from .ExecPin import ExecPin
# from .FloatPin import FloatPin
# from .FloatVector3Pin import FloatVector3Pin
# from .FloatVector4Pin import FloatVector4Pin
# from .IntPin import IntPin
# from .ListPin import ListPin
# from .Matrix33Pin import Matrix33Pin
# from .Matrix44Pin import Matrix44Pin
# from .QuatPin import QuatPin
# from .StringPin import StringPin


# _PINS = {}


# def _REGISTER_PIN_TYPE(pinSubclass):
#     '''
#     registering pin
#     '''
#     dType = pinSubclass.pinDataTypeHint()[0]
#     if dType not in _PINS:
#         _PINS[pinSubclass.pinDataTypeHint()[0]] = pinSubclass
#     else:
#         raise Exception("Error registering pin type {0}\n pin with ID [{1}] already registered".format(pinSubclass.__name__))


# _REGISTER_PIN_TYPE(BoolPin)
# _REGISTER_PIN_TYPE(EnumPin)
# _REGISTER_PIN_TYPE(ExecPin)
# _REGISTER_PIN_TYPE(FloatPin)
# _REGISTER_PIN_TYPE(FloatVector3Pin)
# _REGISTER_PIN_TYPE(FloatVector4Pin)
# _REGISTER_PIN_TYPE(IntPin)
# _REGISTER_PIN_TYPE(ListPin)
# _REGISTER_PIN_TYPE(Matrix33Pin)
# _REGISTER_PIN_TYPE(Matrix44Pin)
# _REGISTER_PIN_TYPE(QuatPin)
# _REGISTER_PIN_TYPE(StringPin)

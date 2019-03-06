PACKAGE_NAME = 'Pyrr'

from PyFlow.Core.Interfaces import IPackage

# Pins
from PyFlow.Packages.Pyrr.Pins.QuatPin import QuatPin
from PyFlow.Packages.Pyrr.Pins.FloatVector3Pin import FloatVector3Pin
from PyFlow.Packages.Pyrr.Pins.FloatVector4Pin import FloatVector4Pin
from PyFlow.Packages.Pyrr.Pins.Matrix33Pin import Matrix33Pin
from PyFlow.Packages.Pyrr.Pins.Matrix44Pin import Matrix44Pin

# Function based nodes
from PyFlow.Packages.Pyrr.FunctionLibraries.Matrix33 import Matrix33
from PyFlow.Packages.Pyrr.FunctionLibraries.Matrix44 import Matrix44
from PyFlow.Packages.Pyrr.FunctionLibraries.QuatLib import QuatLib
from PyFlow.Packages.Pyrr.FunctionLibraries.Vector3 import Vector3
from PyFlow.Packages.Pyrr.FunctionLibraries.Vector4 import Vector4


_FOO_LIBS = {
    Matrix33.__name__: Matrix33(PACKAGE_NAME),
    Matrix44.__name__: Matrix44(PACKAGE_NAME),
    QuatLib.__name__: QuatLib(PACKAGE_NAME),
    Vector3.__name__: Vector3(PACKAGE_NAME),
    Vector4.__name__: Vector4(PACKAGE_NAME)
}

_NODES = {

}

_PINS = {
    FloatVector3Pin.__name__: FloatVector3Pin,
    FloatVector4Pin.__name__: FloatVector4Pin,
    Matrix33Pin.__name__: Matrix33Pin,
    Matrix44Pin.__name__: Matrix44Pin,
    QuatPin.__name__: QuatPin
}


class Pyrr(IPackage):
    def __init__(self):
        super(Pyrr, self).__init__()

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

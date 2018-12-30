from PyFlow.Core.Interfaces import IPackage

# Pins
from PyFlow.Packages.BasePackage.Pins.BoolPin import BoolPin
# TODO: Enums not working for now, fix this.
from PyFlow.Packages.BasePackage.Pins.EnumPin import EnumPin
from PyFlow.Packages.BasePackage.Pins.ExecPin import ExecPin
from PyFlow.Packages.BasePackage.Pins.FloatPin import FloatPin
from PyFlow.Packages.BasePackage.Pins.IntPin import IntPin
from PyFlow.Packages.BasePackage.Pins.ListPin import ListPin
from PyFlow.Packages.BasePackage.Pins.QuatPin import QuatPin
from PyFlow.Packages.BasePackage.Pins.StringPin import StringPin
# TODO: move vector math to separate package
from PyFlow.Packages.BasePackage.Pins.FloatVector3Pin import FloatVector3Pin
from PyFlow.Packages.BasePackage.Pins.FloatVector4Pin import FloatVector4Pin
from PyFlow.Packages.BasePackage.Pins.Matrix33Pin import Matrix33Pin
from PyFlow.Packages.BasePackage.Pins.Matrix44Pin import Matrix44Pin

# Function based nodes
from PyFlow.Packages.BasePackage.FunctionLibraries.ArrayLib import ArrayLib
from PyFlow.Packages.BasePackage.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.BasePackage.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.BasePackage.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.BasePackage.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.BasePackage.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.BasePackage.FunctionLibraries.Matrix33 import Matrix33
from PyFlow.Packages.BasePackage.FunctionLibraries.Matrix44 import Matrix44
from PyFlow.Packages.BasePackage.FunctionLibraries.QuatLib import QuatLib
from PyFlow.Packages.BasePackage.FunctionLibraries.RandomLib import RandomLib
from PyFlow.Packages.BasePackage.FunctionLibraries.Vector3 import Vector3
from PyFlow.Packages.BasePackage.FunctionLibraries.Vector4 import Vector4

# Class based nodes
from PyFlow.Packages.BasePackage.Nodes.branch import branch
from PyFlow.Packages.BasePackage.Nodes.charge import charge
from PyFlow.Packages.BasePackage.Nodes.delay import delay
from PyFlow.Packages.BasePackage.Nodes.deltaTime import deltaTime
from PyFlow.Packages.BasePackage.Nodes.doN import doN
from PyFlow.Packages.BasePackage.Nodes.doOnce import doOnce
from PyFlow.Packages.BasePackage.Nodes.flipFlop import flipFlop
from PyFlow.Packages.BasePackage.Nodes.forLoop import forLoop
from PyFlow.Packages.BasePackage.Nodes.forLoopWithBreak import forLoopWithBreak
from PyFlow.Packages.BasePackage.Nodes.implicitPinCall import implicitPinCall
from PyFlow.Packages.BasePackage.Nodes.retriggerableDelay import retriggerableDelay
from PyFlow.Packages.BasePackage.Nodes.sequence import sequence
from PyFlow.Packages.BasePackage.Nodes.switchOnString import switchOnString
from PyFlow.Packages.BasePackage.Nodes.timer import timer
from PyFlow.Packages.BasePackage.Nodes.whileLoop import whileLoop


_FOO_LIBS = {
    ArrayLib.__name__: ArrayLib(),
    BoolLib.__name__: BoolLib(),
    DefaultLib.__name__: DefaultLib(),
    FloatLib.__name__: FloatLib(),
    IntLib.__name__: IntLib(),
    MathLib.__name__: MathLib(),
    Matrix33.__name__: Matrix33(),
    Matrix44.__name__: Matrix44(),
    QuatLib.__name__: QuatLib(),
    RandomLib.__name__: RandomLib(),
    Vector3.__name__: Vector3(),
    Vector4.__name__: Vector4()
}

_NODES = {
    branch.__name__: branch,
    charge.__name__: charge,
    delay.__name__: delay,
    deltaTime.__name__: deltaTime,
    doN.__name__: doN,
    doOnce.__name__: doOnce,
    flipFlop.__name__: flipFlop,
    forLoop.__name__: forLoop,
    forLoopWithBreak.__name__: forLoopWithBreak,
    implicitPinCall.__name__: implicitPinCall,
    retriggerableDelay.__name__: retriggerableDelay,
    sequence.__name__: sequence,
    switchOnString.__name__: switchOnString,
    timer.__name__: timer,
    whileLoop.__name__: whileLoop
}

_PINS = {
    BoolPin.__name__: BoolPin,
    EnumPin.__name__: EnumPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    FloatVector3Pin.__name__: FloatVector3Pin,
    FloatVector4Pin.__name__: FloatVector4Pin,
    IntPin.__name__: IntPin,
    ListPin.__name__: ListPin,
    Matrix33Pin.__name__: Matrix33Pin,
    Matrix44Pin.__name__: Matrix44Pin,
    QuatPin.__name__: QuatPin,
    StringPin.__name__: StringPin
}


class BasePackage(IPackage):
    def __init__(self):
        super(BasePackage, self).__init__()

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

# Pins
from Pins.BoolPin import BoolPin
# TODO: Enums not working for now, fix this.
from Pins.EnumPin import EnumPin
from Pins.ExecPin import ExecPin
from Pins.FloatPin import FloatPin
from Pins.IntPin import IntPin
from Pins.ListPin import ListPin
from Pins.QuatPin import QuatPin
from Pins.StringPin import StringPin
# TODO: move vector math to separate package
from Pins.FloatVector3Pin import FloatVector3Pin
from Pins.FloatVector4Pin import FloatVector4Pin
from Pins.Matrix33Pin import Matrix33Pin
from Pins.Matrix44Pin import Matrix44Pin

# Function based nodes
from FunctionLibraries.ArrayLib import ArrayLib
from FunctionLibraries.BoolLib import BoolLib
from FunctionLibraries.DefaultLib import DefaultLib
from FunctionLibraries.FloatLib import FloatLib
from FunctionLibraries.IntLib import IntLib
from FunctionLibraries.MathLib import MathLib
from FunctionLibraries.Matrix33 import Matrix33
from FunctionLibraries.Matrix44 import Matrix44
from FunctionLibraries.QuatLib import QuatLib
from FunctionLibraries.RandomLib import RandomLib
from FunctionLibraries.Vector3 import Vector3
from FunctionLibraries.Vector4 import Vector4

# Class based nodes
from Nodes.branch import branch
from Nodes.charge import charge
from Nodes.delay import delay
from Nodes.deltaTime import deltaTime
from Nodes.doN import doN
from Nodes.doOnce import doOnce
from Nodes.flipFlop import flipFlop
from Nodes.forLoop import forLoop
from Nodes.forLoopWithBreak import forLoopWithBreak
from Nodes.implicitPinCall import implicitPinCall
from Nodes.retriggerableDelay import retriggerableDelay
from Nodes.sequence import sequence
from Nodes.switchOnString import switchOnString
from Nodes.timer import timer
from Nodes.whileLoop import whileLoop


__FOO_LIBS = {
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


def GetFunctionLibraries():
    return __FOO_LIBS


def GetNodeClasses():
    return [
        branch,
        charge,
        delay,
        deltaTime,
        doN,
        doOnce,
        flipFlop,
        forLoop,
        forLoopWithBreak,
        implicitPinCall,
        retriggerableDelay,
        sequence,
        switchOnString,
        timer,
        whileLoop
    ]


def GetPinClasses():
    return [
        BoolPin,
        EnumPin,
        ExecPin,
        FloatPin,
        FloatVector3Pin,
        FloatVector4Pin,
        IntPin,
        ListPin,
        Matrix33Pin,
        Matrix44Pin,
        QuatPin,
        StringPin
    ]

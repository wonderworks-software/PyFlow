PACKAGE_NAME = 'PyflowBase'

from PyFlow.Core.Interfaces import IPackage

# Pins
from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyflowBase.Pins.BoolPin import BoolPin
# TODO: Enums not working for now, fix this.
from PyFlow.Packages.PyflowBase.Pins.EnumPin import EnumPin
from PyFlow.Packages.PyflowBase.Pins.ExecPin import ExecPin
from PyFlow.Packages.PyflowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyflowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyflowBase.Pins.StringPin import StringPin

# Function based nodes
from PyFlow.Packages.PyflowBase.FunctionLibraries.ListLib import ListLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathAbstractLib import MathAbstractLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.RandomLib import RandomLib

# Class based nodes
from PyFlow.Packages.PyflowBase.Nodes.branch import branch
from PyFlow.Packages.PyflowBase.Nodes.charge import charge
from PyFlow.Packages.PyflowBase.Nodes.delay import delay
from PyFlow.Packages.PyflowBase.Nodes.deltaTime import deltaTime
from PyFlow.Packages.PyflowBase.Nodes.doN import doN
from PyFlow.Packages.PyflowBase.Nodes.doOnce import doOnce
from PyFlow.Packages.PyflowBase.Nodes.flipFlop import flipFlop
from PyFlow.Packages.PyflowBase.Nodes.forLoop import forLoop
from PyFlow.Packages.PyflowBase.Nodes.forLoopWithBreak import forLoopWithBreak
from PyFlow.Packages.PyflowBase.Nodes.retriggerableDelay import retriggerableDelay
from PyFlow.Packages.PyflowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyflowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyflowBase.Nodes.timer import timer
from PyFlow.Packages.PyflowBase.Nodes.whileLoop import whileLoop
from PyFlow.Packages.PyflowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyflowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyflowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyflowBase.Nodes.reroute import reroute
from PyFlow.Packages.PyflowBase.Nodes.makeList import makeList
from PyFlow.Packages.PyflowBase.Nodes.graphNodes import (
    graphInputs,
    graphOutputs
)
from PyFlow.Packages.PyflowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyflowBase.Nodes.compound import compound

from PyFlow.Packages.PyflowBase.Tools.TestTool import TestTool

_FOO_LIBS = {
    ListLib.__name__: ListLib(PACKAGE_NAME),
    BoolLib.__name__: BoolLib(PACKAGE_NAME),
    DefaultLib.__name__: DefaultLib(PACKAGE_NAME),
    FloatLib.__name__: FloatLib(PACKAGE_NAME),
    IntLib.__name__: IntLib(PACKAGE_NAME),
    MathLib.__name__: MathLib(PACKAGE_NAME),
    MathAbstractLib.__name__: MathAbstractLib(PACKAGE_NAME),
    RandomLib.__name__: RandomLib(PACKAGE_NAME),
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
    retriggerableDelay.__name__: retriggerableDelay,
    sequence.__name__: sequence,
    switchOnString.__name__: switchOnString,
    timer.__name__: timer,
    whileLoop.__name__: whileLoop,
    commentNode.__name__: commentNode,
    getVar.__name__: getVar,
    setVar.__name__: setVar,
    reroute.__name__: reroute,
    graphInputs.__name__: graphInputs,
    graphOutputs.__name__: graphOutputs,
    compound.__name__: compound,
    pythonNode.__name__: pythonNode,
    makeList.__name__: makeList
}

_PINS = {
    AnyPin.__name__: AnyPin,
    BoolPin.__name__: BoolPin,
    EnumPin.__name__: EnumPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    IntPin.__name__: IntPin,
    StringPin.__name__: StringPin
}


_TOOLS = (
    TestTool,
)


class PyflowBase(IPackage):
    def __init__(self):
        super(PyflowBase, self).__init__()

    @staticmethod
    def GetTools():
        return _TOOLS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

PACKAGE_NAME = 'PyflowBase'
from collections import OrderedDict

from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyflowBase.Pins.BoolPin import BoolPin
from PyFlow.Packages.PyflowBase.Pins.ExecPin import ExecPin
from PyFlow.Packages.PyflowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyflowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyflowBase.Pins.StringPin import StringPin
from PyFlow.Packages.PyflowBase.Pins.ListPin import ListPin

# Function based nodes
from PyFlow.Packages.PyflowBase.FunctionLibraries.ArrayLib import ArrayLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.MathAbstractLib import MathAbstractLib
from PyFlow.Packages.PyflowBase.FunctionLibraries.RandomLib import RandomLib

# Class based nodes
from PyFlow.Packages.PyflowBase.Nodes.branch import branch
from PyFlow.Packages.PyflowBase.Nodes.tick import tick
from PyFlow.Packages.PyflowBase.Nodes.charge import charge
from PyFlow.Packages.PyflowBase.Nodes.delay import delay
from PyFlow.Packages.PyflowBase.Nodes.deltaTime import deltaTime
from PyFlow.Packages.PyflowBase.Nodes.doN import doN
from PyFlow.Packages.PyflowBase.Nodes.doOnce import doOnce
from PyFlow.Packages.PyflowBase.Nodes.flipFlop import flipFlop
from PyFlow.Packages.PyflowBase.Nodes.forLoop import forLoop
from PyFlow.Packages.PyflowBase.Nodes.forEachLoop import forEachLoop
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
from PyFlow.Packages.PyflowBase.Nodes.rerouteExecs import rerouteExecs
from PyFlow.Packages.PyflowBase.Nodes.makeArray import makeArray
from PyFlow.Packages.PyflowBase.Nodes.makeList import makeList
from PyFlow.Packages.PyflowBase.Nodes.consoleOutput import consoleOutput
from PyFlow.Packages.PyflowBase.Nodes.address import address
from PyFlow.Packages.PyflowBase.Nodes.graphNodes import (
    graphInputs,
    graphOutputs
)
from PyFlow.Packages.PyflowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyflowBase.Nodes.compound import compound
from PyFlow.Packages.PyflowBase.Nodes.constant import constant

from PyFlow.Packages.PyflowBase.Tools.ScreenshotTool import ScreenshotTool
from PyFlow.Packages.PyflowBase.Tools.NodeBoxTool import NodeBoxTool
from PyFlow.Packages.PyflowBase.Tools.SearchResultsTool import SearchResultsTool
from PyFlow.Packages.PyflowBase.Tools.AlignLeftTool import AlignLeftTool
from PyFlow.Packages.PyflowBase.Tools.AlignRightTool import AlignRightTool
from PyFlow.Packages.PyflowBase.Tools.AlignTopTool import AlignTopTool
from PyFlow.Packages.PyflowBase.Tools.AlignBottomTool import AlignBottomTool
from PyFlow.Packages.PyflowBase.Tools.HistoryTool import HistoryTool
from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool
from PyFlow.Packages.PyflowBase.Tools.VariablesTool import VariablesTool

from PyFlow.Packages.PyflowBase.Exporters.PythonScriptExporter import PythonScriptExporter
from PyFlow.Packages.PyflowBase.Exporters.CPPCompiler import CPPCompiler

# Factories
from PyFlow.Packages.PyflowBase.Factories.UIPinFactory import createUIPin
from PyFlow.Packages.PyflowBase.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.PyflowBase.Factories.UINodeFactory import createUINode


_FOO_LIBS = {
    ArrayLib.__name__: ArrayLib(PACKAGE_NAME),
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
    rerouteExecs.__name__: rerouteExecs,
    graphInputs.__name__: graphInputs,
    graphOutputs.__name__: graphOutputs,
    compound.__name__: compound,
    pythonNode.__name__: pythonNode,
    makeArray.__name__: makeArray,
    makeList.__name__: makeList,
    consoleOutput.__name__: consoleOutput,
    forEachLoop.__name__: forEachLoop,
    address.__name__: address,
    constant.__name__: constant,
    tick.__name__: tick
}

_PINS = {
    AnyPin.__name__: AnyPin,
    BoolPin.__name__: BoolPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    IntPin.__name__: IntPin,
    StringPin.__name__: StringPin,
    ListPin.__name__: ListPin
}

# Toolbar will be created in following order
_TOOLS = OrderedDict()
_TOOLS[ScreenshotTool.__name__] = ScreenshotTool
_TOOLS[AlignLeftTool.__name__] = AlignLeftTool
_TOOLS[AlignRightTool.__name__] = AlignRightTool
_TOOLS[AlignTopTool.__name__] = AlignTopTool
_TOOLS[AlignBottomTool.__name__] = AlignBottomTool
_TOOLS[HistoryTool.__name__] = HistoryTool
_TOOLS[PropertiesTool.__name__] = PropertiesTool
_TOOLS[VariablesTool.__name__] = VariablesTool
_TOOLS[NodeBoxTool.__name__] = NodeBoxTool
_TOOLS[SearchResultsTool.__name__] = SearchResultsTool


_EXPORTERS = OrderedDict()
_EXPORTERS[PythonScriptExporter.__name__] = PythonScriptExporter
_EXPORTERS[CPPCompiler.__name__] = CPPCompiler


class PyflowBase(IPackage):
    def __init__(self):
        super(PyflowBase, self).__init__()

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetToolClasses():
        return _TOOLS

    @staticmethod
    def UIPinsFactory():
        return createUIPin

    @staticmethod
    def UINodesFactory():
        return createUINode

    @staticmethod
    def PinsInputWidgetFactory():
        return getInputWidget

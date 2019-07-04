"""Base package
"""
PACKAGE_NAME = 'PyFlowBase'
from collections import OrderedDict

from PyFlow.UI.UIInterfaces import IPackage

# Pins
from PyFlow.Packages.PyFlowBase.Pins.AnyPin import AnyPin
from PyFlow.Packages.PyFlowBase.Pins.BoolPin import BoolPin
from PyFlow.Packages.PyFlowBase.Pins.ExecPin import ExecPin
from PyFlow.Packages.PyFlowBase.Pins.FloatPin import FloatPin
from PyFlow.Packages.PyFlowBase.Pins.IntPin import IntPin
from PyFlow.Packages.PyFlowBase.Pins.StringPin import StringPin

# Function based nodes
from PyFlow.Packages.PyFlowBase.FunctionLibraries.ArrayLib import ArrayLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.BoolLib import BoolLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.DefaultLib import DefaultLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.FloatLib import FloatLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.IntLib import IntLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.MathLib import MathLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.MathAbstractLib import MathAbstractLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.RandomLib import RandomLib
from PyFlow.Packages.PyFlowBase.FunctionLibraries.PathLib import PathLib

# Class based nodes
from PyFlow.Packages.PyFlowBase.Nodes.branch import branch
from PyFlow.Packages.PyFlowBase.Nodes.tick import tick
from PyFlow.Packages.PyFlowBase.Nodes.charge import charge
from PyFlow.Packages.PyFlowBase.Nodes.delay import delay
from PyFlow.Packages.PyFlowBase.Nodes.deltaTime import deltaTime
from PyFlow.Packages.PyFlowBase.Nodes.doN import doN
from PyFlow.Packages.PyFlowBase.Nodes.doOnce import doOnce
from PyFlow.Packages.PyFlowBase.Nodes.flipFlop import flipFlop
from PyFlow.Packages.PyFlowBase.Nodes.forLoop import forLoop
from PyFlow.Packages.PyFlowBase.Nodes.forEachLoop import forEachLoop
from PyFlow.Packages.PyFlowBase.Nodes.forLoopWithBreak import forLoopWithBreak
from PyFlow.Packages.PyFlowBase.Nodes.retriggerableDelay import retriggerableDelay
from PyFlow.Packages.PyFlowBase.Nodes.sequence import sequence
from PyFlow.Packages.PyFlowBase.Nodes.switchOnString import switchOnString
from PyFlow.Packages.PyFlowBase.Nodes.timer import timer
from PyFlow.Packages.PyFlowBase.Nodes.whileLoop import whileLoop
from PyFlow.Packages.PyFlowBase.Nodes.getVar import getVar
from PyFlow.Packages.PyFlowBase.Nodes.setVar import setVar
from PyFlow.Packages.PyFlowBase.Nodes.reroute import reroute
from PyFlow.Packages.PyFlowBase.Nodes.rerouteExecs import rerouteExecs
from PyFlow.Packages.PyFlowBase.Nodes.makeArray import makeArray
from PyFlow.Packages.PyFlowBase.Nodes.makeList import makeList
from PyFlow.Packages.PyFlowBase.Nodes.makeDict import makeDict
from PyFlow.Packages.PyFlowBase.Nodes.makeAnyDict import makeAnyDict
from PyFlow.Packages.PyFlowBase.Nodes.makeDictElement import makeDictElement
from PyFlow.Packages.PyFlowBase.Nodes.dictKeys import dictKeys
from PyFlow.Packages.PyFlowBase.Nodes.floatRamp import floatRamp
from PyFlow.Packages.PyFlowBase.Nodes.colorRamp import colorRamp
from PyFlow.Packages.PyFlowBase.Nodes.stringToArray import stringToArray


from PyFlow.Packages.PyFlowBase.Nodes.consoleOutput import consoleOutput
from PyFlow.Packages.PyFlowBase.Nodes.address import address
from PyFlow.Packages.PyFlowBase.Nodes.graphNodes import graphInputs, graphOutputs
from PyFlow.Packages.PyFlowBase.Nodes.pythonNode import pythonNode
from PyFlow.Packages.PyFlowBase.Nodes.compound import compound
from PyFlow.Packages.PyFlowBase.Nodes.constant import constant
from PyFlow.Packages.PyFlowBase.Nodes.convertTo import convertTo
from PyFlow.Packages.PyFlowBase.Nodes.imageDisplay import imageDisplay


from PyFlow.Packages.PyFlowBase.Nodes.commentNode import commentNode
from PyFlow.Packages.PyFlowBase.Nodes.stickyNote import stickyNote

from PyFlow.Packages.PyFlowBase.Tools.ScreenshotTool import ScreenshotTool
from PyFlow.Packages.PyFlowBase.Tools.NodeBoxTool import NodeBoxTool
from PyFlow.Packages.PyFlowBase.Tools.SearchResultsTool import SearchResultsTool
from PyFlow.Packages.PyFlowBase.Tools.AlignLeftTool import AlignLeftTool
from PyFlow.Packages.PyFlowBase.Tools.AlignRightTool import AlignRightTool
from PyFlow.Packages.PyFlowBase.Tools.AlignTopTool import AlignTopTool
from PyFlow.Packages.PyFlowBase.Tools.AlignBottomTool import AlignBottomTool
from PyFlow.Packages.PyFlowBase.Tools.HistoryTool import HistoryTool
from PyFlow.Packages.PyFlowBase.Tools.PropertiesTool import PropertiesTool
from PyFlow.Packages.PyFlowBase.Tools.VariablesTool import VariablesTool
from PyFlow.Packages.PyFlowBase.Tools.CompileTool import CompileTool
from PyFlow.Packages.PyFlowBase.Tools.LoggerTool import LoggerTool

from PyFlow.Packages.PyFlowBase.Exporters.PythonScriptExporter import PythonScriptExporter
from PyFlow.Packages.PyFlowBase.Exporters.CPPCompiler import CPPCompiler

# Factories
from PyFlow.Packages.PyFlowBase.Factories.UIPinFactory import createUIPin
from PyFlow.Packages.PyFlowBase.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.PyFlowBase.Factories.UINodeFactory import createUINode

from PyFlow.Packages.PyFlowBase.PrefsWidgets.General import GeneralPreferences
from PyFlow.Packages.PyFlowBase.PrefsWidgets.InputPrefs import InputPreferences
from PyFlow.Packages.PyFlowBase.PrefsWidgets.ThemePrefs import ThemePreferences


_FOO_LIBS = {
    ArrayLib.__name__: ArrayLib(PACKAGE_NAME),
    BoolLib.__name__: BoolLib(PACKAGE_NAME),
    DefaultLib.__name__: DefaultLib(PACKAGE_NAME),
    FloatLib.__name__: FloatLib(PACKAGE_NAME),
    IntLib.__name__: IntLib(PACKAGE_NAME),
    MathLib.__name__: MathLib(PACKAGE_NAME),
    MathAbstractLib.__name__: MathAbstractLib(PACKAGE_NAME),
    RandomLib.__name__: RandomLib(PACKAGE_NAME),
    PathLib.__name__ : PathLib(PACKAGE_NAME),
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
    stickyNote.__name__ : stickyNote,
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
    makeDict.__name__: makeDict,
    makeAnyDict.__name__: makeAnyDict,
    makeDictElement.__name__: makeDictElement,
    consoleOutput.__name__: consoleOutput,
    forEachLoop.__name__: forEachLoop,
    address.__name__: address,
    constant.__name__: constant,
    tick.__name__: tick,
    convertTo.__name__: convertTo,
    dictKeys.__name__: dictKeys,
    floatRamp.__name__: floatRamp,
    colorRamp.__name__: colorRamp,
    stringToArray.__name__:stringToArray,
    imageDisplay.__name__ : imageDisplay
}

_PINS = {
    AnyPin.__name__: AnyPin,
    BoolPin.__name__: BoolPin,
    ExecPin.__name__: ExecPin,
    FloatPin.__name__: FloatPin,
    IntPin.__name__: IntPin,
    StringPin.__name__: StringPin,
}

# Toolbar will be created in following order
_TOOLS = OrderedDict()
_TOOLS[CompileTool.__name__] = CompileTool
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
_TOOLS[LoggerTool.__name__] = LoggerTool

_EXPORTERS = OrderedDict()
_EXPORTERS[PythonScriptExporter.__name__] = PythonScriptExporter
_EXPORTERS[CPPCompiler.__name__] = CPPCompiler


_PREFS_WIDGETS = OrderedDict()
_PREFS_WIDGETS["General"] = GeneralPreferences
_PREFS_WIDGETS["Input"] = InputPreferences
_PREFS_WIDGETS["Theme"] = ThemePreferences


class PyFlowBase(IPackage):
    """Base pyflow package
    """
    def __init__(self):
        super(PyFlowBase, self).__init__()

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

    @staticmethod
    def PrefsWidgets():
        return _PREFS_WIDGETS

"""@file Common.py

**Common.py** is a common definitions file

this file is imported in almost all others files of the program
"""
import re
import math
import time
import inspect
import struct
import weakref
try:
    from queue import Queue
except:
    from Queue import Queue
import uuid
import sys

from nine import IS_PYTHON2, str
if IS_PYTHON2:
    from aenum import IntEnum, Flag, auto
else:
    from enum import IntEnum, Flag, auto

from PyFlow import findPinClassByType
from PyFlow.Core.version import Version


maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1


FLOAT_RANGE_MIN = 0.1 + (-maxint - 1.0)
FLOAT_RANGE_MAX = maxint + 0.1
INT_RANGE_MIN = -maxint + 0
INT_RANGE_MAX = maxint + 0

DEFAULT_IN_EXEC_NAME = str('inExec')
DEFAULT_OUT_EXEC_NAME = str('outExec')


## Performs a linear interpolation
# @param[in] start the value to interpolate from
# @param[in] end the value to interpolate to
# @param[in] alpha how far to interpolate
# @returns The result of the linear interpolation (float)
def lerp(start, end, alpha):
    return (start + alpha * (end - start))


## Calculates the percentage along a line from MinValue to MaxValue that Value is.
def GetRangePct(MinValue, MaxValue, Value):
    return (Value - MinValue) / (MaxValue - MinValue)


def sign(x):
    return x and (1, -1)[x < 0]


## Computes the value of the first specified argument clamped to a range defined by the second and third specified arguments
# @param[in] n
# @param[in] vmin
# @param[in] vmax
# @returns The clamped value of n
def clamp(n, vmin, vmax):
    return max(min(n, vmax), vmin)


## Rounding up to sertain value. Used in grid snapping
# @param[in] x value to round
# @param[in] to value x will be rounded to
# @returns rounded value of x
def roundup(x, to):
    return int(math.ceil(x / to)) * to


## Clearing a list in python previous to 3.2 is not possible with list.clear()
# @param[in] list list to clear
# @returns cleared List
currentVersion = Version(sys.version_info.major, sys.version_info.minor, 0)
python32 = Version(3, 2, 0)
if currentVersion <= python32:
    def clearList(list):
        del list[:]
else:
    def clearList(list):
        list.clear()


def findGoodId(ids):
    """Finds good minimum unique int from iterable. Starting from 1

    Arguments:
        ids {list|set|tuple} -- a collection of occupied ids

    Returns:
        [int]
    """

    if len(ids) == 0:
        return 1

    ids = sorted(set(ids))
    lastID = min(ids)

    if lastID > 1:
        return 1

    for ID in ids:
        diff = ID - lastID
        if diff > 1:
            return lastID + 1
            break
        lastID = ID
    else:
        return ID + 1


def wrapStringToFunctionDef(functionName, scriptString, kwargs=None):
    """wrapStringToFunctionDef Generates function string

    example: wrapStringToFunctionDef('test', 'print(a)', {'a': 5})

    def test(a=5):
        print(a)
    """
    kwargsString = ""
    if kwargs is not None:
        for argname, argValue in kwargs.items():
            if isinstance(argValue, str):
                argValue = "'{}'".format(argValue)
            kwargsString += "{0}={1}, ".format(argname, argValue)
        kwargsString = kwargsString[:-2]

    result = "def {0}({1}):\n".format(functionName, kwargsString)

    for scriptLine in scriptString.split('\n'):
        result += "\t{}".format(scriptLine)
        result += '\n'
    return result


## Check for cycle connected nodes
# @param[in] left hand side pin
# @param[in] right hand side pin
# @returns bool
def cycle_check(src, dst):
    if src.direction == PinDirection.Input:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycle_check(start, i):
            return True
    return False


def arePinsConnected(src, dst):
    """Checks if two pins are connected

    Arguments:
        src PinBase -- left hand side pin
        dst PinBase -- right hand side pin
    """
    if src.direction == dst.direction:
        return False
    if src.owningNode() == dst.owningNode():
        return False
    if src.direction == PinDirection.Input:
        src, dst = dst, src
    if dst in src.affects and src in dst.affected_by:
        return True
    return False


def getConnectedPins(pin):
    result = set()
    if pin.direction == PinDirection.Input:
        for lhsPin in pin.affected_by:
            result.add(lhsPin)
    if pin.direction == PinDirection.Output:
        for rhsPin in pin.affects:
            result.add(rhsPin)
    return result


## This function for establish dependencies bitween pins
def pinAffects(lhs, rhs):
    assert(lhs is not rhs), "pin can not affect itself"
    lhs.affects.add(rhs)
    rhs.affected_by.add(lhs)


def canConnectPins(src, dst):
    if src is None or dst is None:
        return False

    if src.direction == dst.direction:
        return False

    if arePinsConnected(src, dst):
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src

    if cycle_check(src, dst):
        return False

    if src.isExec() and dst.isExec():
        return True

    if not src.isArray() and dst.isArray():
        if dst.optionEnabled(PinOptions.SupportsOnlyArrays) and not (src.canChangeStructure(dst._currStructure, []) or dst.canChangeStructure(src._currStructure, [], selfChek=False)):
            return False

    if not src.isDict() and dst.isDict():
        if dst.optionEnabled(PinOptions.SupportsOnlyArrays) and not (src.canChangeStructure(dst._currStructure, []) or dst.canChangeStructure(src._currStructure, [], selfChek=False)):
            return False
        elif not src.supportDictElement([],src.optionEnabled(PinOptions.DictElementSuported)):#:
            return False
        else:
            dictElement = src.getDictElementNode([])
            dictNode = dst.getDictNode([])
            nodeFree = False
            if dictNode:
                nodeFree = dictNode.KeyType.checkFree([])
            if dictElement:
                if not dictElement.key.checkFree([]) and not nodeFree:
                    if dst._data.keyType != dictElement.key.dataType:
                        return False

    if src.isArray() and not dst.isArray():
        srcCanChangeStruct = src.canChangeStructure(dst._currStructure, [])
        dstCanCnahgeStruct = dst.canChangeStructure(src._currStructure, [], selfChek=False)
        if not dst.optionEnabled(PinOptions.ArraySupported) and not (srcCanChangeStruct or dstCanCnahgeStruct):
            return False

    if src.isDict() and not dst.isDict():
        srcCanChangeStruct = src.canChangeStructure(dst._currStructure, [])
        dstCanCnahgeStruct = dst.canChangeStructure(src._currStructure, [], selfChek=False)
        if not dst.optionEnabled(PinOptions.DictSupported) and not (srcCanChangeStruct or dstCanCnahgeStruct):
            return False

    if dst.hasConnections():
        if not dst.optionEnabled(PinOptions.AllowMultipleConnections) and dst.reconnectionPolicy == PinReconnectionPolicy.ForbidConnection:
            return False

    if src.hasConnections():
        if not src.optionEnabled(PinOptions.AllowMultipleConnections) and src.reconnectionPolicy == PinReconnectionPolicy.ForbidConnection:
            return False

    if src.owningNode().graph() is None or dst.owningNode().graph() is None:
        return False

    if src.isAny() and dst.isExec():
        if src.dataType not in dst.supportedDataTypes():
            return False

    if src.isExec() and not dst.isExec():
        return False

    if not src.isExec() and dst.isExec():
        return False

    if src.IsValuePin() and dst.IsValuePin():
        if src.dataType in dst.allowedDataTypes([], dst._supportedDataTypes) or dst.dataType in src.allowedDataTypes([], src._supportedDataTypes):
            if all([src.dataType == "AnyPin" and not src.canChangeTypeOnConection([], src.optionEnabled(PinOptions.ChangeTypeOnConnection), []),
                    (dst.canChangeTypeOnConection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []) and not dst.optionEnabled(PinOptions.AllowAny) or not dst.canChangeTypeOnConection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []))]):
                return False
            if not src.isDict() and dst.supportOnlyDictElement([],dst.isDict()):
                if not src.supportDictElement([],src.optionEnabled(PinOptions.DictElementSuported)) and dst.supportOnlyDictElement([],dst.isDict()):
                    return False 
            return True
        else:
            if all([src.dataType in list(dst.allowedDataTypes([], dst._defaultSupportedDataTypes, selfChek=dst.optionEnabled(PinOptions.AllowMultipleConnections), defaults=True)) + ["AnyPin"],
                   dst.checkFree([], selfChek=dst.optionEnabled(PinOptions.AllowMultipleConnections))]):
                return True
            if all([dst.dataType in list(src.allowedDataTypes([], src._defaultSupportedDataTypes, defaults=True)) + ["AnyPin"],
                   src.checkFree([])]):
                return True
        return False

    if src.owningNode == dst.owningNode:
        return False

    return True


def connectPins(src, dst):
    """Connects two pins

    Arguments:
        src PinBase -- left hand side pin
        dst PinBase -- right hand side pin
    """
    if src.direction == PinDirection.Input:
        src, dst = dst, src

    if not canConnectPins(src, dst):
        return False

    # input value pins can have one output connection if `AllowMultipleConnections` flag is disabled
    # output value pins can have any number of connections
    if src.IsValuePin() and dst.IsValuePin():
        if dst.hasConnections():
            if not dst.optionEnabled(PinOptions.AllowMultipleConnections):
                dst.disconnectAll()

    # input execs can have any number of connections
    # output execs can have only one connection
    if src.isExec() and dst.isExec():
        if src.hasConnections():
            if not src.optionEnabled(PinOptions.AllowMultipleConnections):
                src.disconnectAll()

    if src.isExec() and dst.isExec():
        src.onExecute.connect(dst.call)

    dst.aboutToConnect(src)
    src.aboutToConnect(dst)

    pinAffects(src, dst)
    src.setDirty()

    dst.setData(src.currentData())

    dst.pinConnected(src)
    src.pinConnected(dst)
    push(dst)
    return True


def connectPinsByIndexes(lhsNode=None, lhsOutPinIndex=0, rhsNode=None, rhsInPinIndex=0):
    if lhsNode is None:
        return False

    if rhsNode is None:
        return False

    if lhsOutPinIndex not in lhsNode.orderedOutputs:
        return False

    if rhsInPinIndex not in rhsNode.orderedInputs:
        return False

    lhsPin = lhsNode.orderedOutputs[lhsOutPinIndex]
    rhsPin = rhsNode.orderedInputs[rhsInPinIndex]

    return connectPins(lhsPin, rhsPin)


def traverseNeighborPins(startFrom, callback):
    """Iterates over all neighbor pins and passes pin into callback function. Callback will be executed once for every pin
    """

    traversed = set()

    def worker(pin):
        if pin not in traversed:
            traversed.add(pin)
            callback(pin)
            nodePins = pin.owningNode().pins.copy()
            for connectedPin in getConnectedPins(pin):
                if connectedPin in traversed:
                    continue
                nodePins.add(connectedPin)
            for neighbor in list(nodePins):
                if neighbor not in traversed:
                    worker(neighbor)
    worker(startFrom)


def traverseConstrainedPins(startFrom, callback):
    """Iterates over all constrained chained pins of type `Any` and passes pin into callback function. Callback will be executed once for every pin
    """
    if not startFrom.isAny():
        return
    traversed = set()

    def worker(pin):
        traversed.add(pin)
        callback(pin)

        if pin.constraint is None:
            return
        nodePins = set(pin.owningNode().constraints[pin.constraint])
        for connectedPin in getConnectedPins(pin):
            if connectedPin.isAny():
                nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                worker(neighbor)

    worker(startFrom)


def traverseStructConstrainedPins(startFrom, callback):
    """Iterates over all constrained chained pins passes pin into callback function. Callback will be executed once for every pin
    """
    traversed = set()

    def worker(pin):
        traversed.add(pin)
        callback(pin)
        nodePins = set()
        if pin.structConstraint is not None:
            nodePins = set(pin.owningNode().structConstraints[pin.structConstraint])
        for connectedPin in getConnectedPins(pin):
            nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                worker(neighbor)

    worker(startFrom)


def disconnectPins(src, dst):
    """Disconnects two pins

    Arguments:
        src PinBase -- left hand side pin
        dst PinBase -- right hand side pin
    """
    if arePinsConnected(src, dst):
        if src.direction == PinDirection.Input:
            src, dst = dst, src
        src.affects.remove(dst)
        dst.affected_by.remove(src)
        src.pinDisconnected(dst)
        dst.pinDisconnected(src)
        push(dst)
        if src.isExec() and dst.isExec():
            src.onExecute.disconnect(dst.call)
        return True
    return False


## marks dirty all ports from start to the right
# this part of graph will be recomputed every tick
# @param[in] start_from pin from which recursion begins
def push(start_from):
    if not len(start_from.affects) == 0:
        start_from.setDirty()
        for i in start_from.affects:
            i.setDirty()
            push(i)


def extractDigitsFromEndOfString(string):
    result = re.search('(\d+)$', string)
    if result is not None:
        return int(result.group(0))


def removeDigitsFromEndOfString(string):
    return re.sub(r'\d+$', '', string)


def getUniqNameFromList(existingNames, name):
    if name not in existingNames:
        return name
    ids = set()
    for existingName in existingNames:
        digits = extractDigitsFromEndOfString(existingName)
        if digits is not None:
            ids.add(digits)
    idx = findGoodId(ids)
    nameNoDigits = removeDigitsFromEndOfString(name)
    return nameNoDigits + str(idx)


def clearSignal(signal):
    """Disconnects all receivers

    Arguments:
        signal {Signal} -- blinker Signal class
    """
    for receiver in list(signal.receivers.values()):
        if isinstance(receiver, weakref.ref):
            signal.disconnect(receiver())
        else:
            signal.disconnect(receiver)


class SingletonDecorator:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


class dictElement(tuple):
    def __new__(self, a=None, b=None):
        if a is None and b is None:
            new = ()
        elif b is None:
            if isinstance(a, tuple) and len(a) <= 2:
                new = a
            else:
                raise Exception("non Valid Input")
        else:
            new = (a, b)
        return super(dictElement, self).__new__(self, new)


class pyf_dict(dict):
    def __init__(self, keyType, valueType=None, inpt={}):
        super(pyf_dict, self).__init__(inpt)
        self.keyType = keyType
        self.valueType = valueType

    def __setitem__(self, key, item):
        if type(key) == self.getClassFromType(self.keyType): # and type(item) == self.getClassFromType(self.valueType):
            super(pyf_dict, self).__setitem__(key, item)
        else:
            raise Exception(
                "Valid key should be a {0}".format(self.getClassFromType(self.keyType)))

    def getClassFromType(self, pinType):
        pin = findPinClassByType(pinType)
        if pin:
            pinClass = pin.internalDataStructure()
            return pinClass
        return None

class PinReconnectionPolicy(IntEnum):
    DisconnectIfHasConnections = 0
    ForbidConnection = 1


class PinOptions(Flag):
    ArraySupported = auto()
    DictSupported = auto()
    SupportsOnlyArrays = auto()
    AllowMultipleConnections = auto()
    ChangeTypeOnConnection = auto()
    RenamingEnabled = auto()
    Dynamic = auto()
    AlwaysPushDirty = auto()
    Storable = auto()
    AllowAny = auto()
    DictElementSuported = auto()

# Used for determine Pin Structure Type
class PinStructure(IntEnum):
    Single = 0
    Array = 1
    Dict = 2
    Multi = 3


def findStructFromValue(value):
    if isinstance(value, list):
        return PinStructure.Array
    if isinstance(value, dict):
        return PinStructure.Dict
    return PinStructure.Single


# Used in PyFlow.AbstractGraph.NodeBase.getPin for optimization purposes
class PinSelectionGroup(IntEnum):
    Inputs = 0
    Outputs = 1
    BothSides = 2


## Can be used for code generation
class AccessLevel(IntEnum):
    public = 0
    private = 1
    protected = 2


## Determines whether it is input pin or output.
class PinDirection(IntEnum):
    Input = 0
    Output = 1


## Determines whether it is callable node or pure.
# Callable node is a node with Exec pins
class NodeTypes(IntEnum):
    Callable = 0
    Pure = 1


## Direction identifiers. Used in [alignSelectedNodes](@ref PyFlow.Core.Widget.GraphWidget.alignSelectedNodes)
class Direction(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

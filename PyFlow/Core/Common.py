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
from enum import IntEnum
from PyFlow import findPinClassByType

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1

FLOAT_RANGE_MIN = 0.1 + (-maxint - 1.0)
FLOAT_RANGE_MAX = maxint + 0.1
INT_RANGE_MIN = -maxint + 0
INT_RANGE_MAX = maxint + 0

DEFAULT_IN_EXEC_NAME = 'inExec'
DEFAULT_OUT_EXEC_NAME = 'outExec'


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
    if src.owningNode() == dst.owningNode():
        return False
    if src.direction == dst.direction:
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
        # print("can not connect pins")
        # if src is None:
        #     print("src is None")
        # if dst is None:
        #     print("dst is None")
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src

    if src.direction == dst.direction:
        # print("same direction pins can't be connected")
        return False

    if dst.isList() and not src.isList():
        if dst.supportsOnlyList:
            # print("dst supports only arrays")
            return False

    if src.isList() and not dst.isList():
        if not dst.listSupported:
            return False

    if src.owningNode().graph() is None or dst.owningNode().graph() is None:
        return False

    if cycle_check(src, dst):
        # print('cycles are not allowed')
        return False

    if src.dataType == "AnyPin" and not cycle_check(src, dst):
        # print("cycle detected")
        return True

    if dst.isAny():
        if src.dataType not in findPinClassByType(dst.activeDataType).supportedDataTypes():
            # print("type is not supported")
            return False

    if src.isExec() and not dst.isExec():
        return False

    if src.dataType not in dst.supportedDataTypes() and not src.dataType == "AnyPin":
        # print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
        return False
    else:
        if src.dataType is 'ExecPin':
            if dst.dataType != 'ExecPin' and dst.dataType != 'AnyPin':
                # print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
                return False

    if src in dst.affected_by:
        # print('already connected. skipped')
        return False
    if src.direction == dst.direction:
        # print('same side pins can not be connected')
        return False
    if src.owningNode == dst.owningNode:
        # print('can not connect to owning node')
        return False

    if dst.constraint is not None:
        if dst.dataType != "AnyPin":
            if dst.isAny():
                free = dst.checkFree([], False)
                if not free:
                    pinClass = findPinClassByType(dst.dataType)
                    if src.dataType not in pinClass.supportedDataTypes():
                        # print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
                        return False
    return True


def connectPins(src, dst):
    """Connects two pins

    Arguments:
        src PinBase -- left hand side pin
        dst PinBase -- right hand side pin
    """
    if not canConnectPins(src, dst):
        return False

    if arePinsConnected(src, dst):
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src

    if dst.hasConnections() and not dst.isAllowMultiConnection():
        dst.disconnectAll()

    # input value pins can have one output connection if right hand side is not an list
    # output value pins can have any number of connections
    if src.dataType not in ['ExecPin', 'AnyPin'] and dst.hasConnections():
        if not dst.isAllowMultiConnection():
            dst.disconnectAll()
    if src.dataType == 'AnyPin' and dst.dataType != 'ExecPin' and dst.hasConnections():
        if not dst.isAllowMultiConnection():
            dst.disconnectAll()
    # input execs can have any number of connections
    # output execs can have only one connection
    if src.isExec() and dst.isExec() and src.hasConnections():
        if not src.isAllowMultiConnection():
            src.disconnectAll()

    if src.isExec() and dst.isExec():
        src.onExecute.connect(dst.call)

    pinAffects(src, dst)
    src.setDirty()

    dst._data = src.currentData()

    dst.pinConnected(src)
    src.pinConnected(dst)
    push(dst)
    return True


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


# For any pin. setAsList on connected/disconnected or not
class ListSwitchPolicy(IntEnum):
    Auto = 0
    DoNotSwitch = 1


## Used in PyFlow.AbstractGraph.NodeBase.getPin for optimization purposes
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

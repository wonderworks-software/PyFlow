"""@file Common.py

**Common.py** is a common definitions file

this file is imported in almost all others files of the program
"""
import math
import time
import inspect
import struct
import weakref
from treelib import Node, Tree
try:
    from queue import Queue
except:
    from Queue import Queue
import uuid
import sys
from enum import IntEnum
from PyFlow.Core import Enums
from PyFlow import findPinClassByType

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1

FLOAT_RANGE_MIN = 0.1 + (-maxint - 1.0)
FLOAT_RANGE_MAX = maxint + 0.1
INT_RANGE_MIN = -maxint + 0
INT_RANGE_MAX = maxint + 0

## Used in function library decorator to mark pins as always dirty
# for example random integer node should always mark dirty all upper branches of graph
PROPAGATE_DIRTY = 'PropagateDirty'

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
        return False

    if src.owningNode().graph() is None or dst.owningNode().graph() is None:
        return False

    if cycle_check(src, dst):
        # print('cycles are not allowed')
        return False

    if src.dataType == "AnyPin" and not cycle_check(src, dst):
        return True

    if dst.dataType == "AnyPin":
        if src.dataType not in findPinClassByType(dst.activeDataType).supportedDataTypes():
            return False

    if dst.isAny:
        if src.dataType not in findPinClassByType(dst.dataType).supportedDataTypes():
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
            if dst.isAny:
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
    if arePinsConnected(src, dst):
        return False

    if not canConnectPins(src, dst):
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src

    # input value pins can have one output connection
    # output value pins can have any number of connections
    if src.dataType not in ['ExecPin', 'AnyPin'] and dst.hasConnections():
        dst.disconnectAll()
    if src.dataType == 'AnyPin' and dst.dataType != 'ExecPin' and dst.hasConnections():
        dst.disconnectAll()
    # input execs can have any number of connections
    # output execs can have only one connection
    if src.dataType == 'ExecPin' and dst.dataType == 'ExecPin' and src.hasConnections():
        src.disconnectAll()

    if src.dataType == 'ExecPin' and dst.dataType == 'ExecPin':
        src.onExecute.connect(dst.call)

    pinAffects(src, dst)
    src.setDirty()
    dst._data = src.currentData()
    dst.pinConnected(src)
    src.pinConnected(dst)
    push(dst)
    src._linkedToUids.add(dst.uid)
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
        src._linkedToUids.remove(dst.uid)
        if src.dataType == 'ExecPin' and dst.dataType == 'ExecPin':
            src.onExecute.disconnect(dst.call)
        return True
    return False


## marks dirty all ports from start to the right
# this part of graph will be recomputed every tick
# @param[in] start_from pin from which recursion begins
def push(start_from):
    if not start_from.affects == []:
        start_from.setDirty()
        for i in start_from.affects:
            i.setDirty()
            push(i)


## This function clears property view's layout.
# @param[in] layout QLayout class
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def getUniqNameFromList(existingNames, name):
    # TODO: Extract digits from node and find good Id
    if name not in existingNames:
        return name
    idx = 0
    tmp = name
    while tmp in existingNames:
        idx += 1
        tmp = name + str(idx)
    return name + str(idx)


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


class REGISTER_ENUM(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls):
        Enums.appendEnumInstance(cls)
        return cls


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


@REGISTER_ENUM()
## Direction identifiers. Used in [alignSelectedNodes](@ref PyFlow.Core.Widget.GraphWidget.alignSelectedNodes)
class Direction(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

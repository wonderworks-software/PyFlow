"""@file Common.py

**Common.py** is a common definitions file

this file is imported in almost all others files of the program
"""
import math
import time
import inspect
import struct
try:
    from queue import Queue
except:
    from Queue import Queue
import uuid
import sys
from enum import IntEnum
from PyFlow.Core import Enums

maxint = 2 ** (struct.Struct('i').size * 8 - 1) - 1

FLOAT_RANGE_MIN = 0.1 + (-maxint - 1.0)
FLOAT_RANGE_MAX = maxint + 0.1
INT_RANGE_MIN = -maxint + 0
INT_RANGE_MAX = maxint + 0

# TODO: Move to config
GRID_SIZE = 20

## Used in function library decorator to mark pins as always dirty
# for example random integer node should always mark dirty all upper branches of graph
PROPAGATE_DIRTY = 'PropagateDirty'


## Performs a linear interpolation
# @param[in] start the value to interpolate from
# @param[in] end the value to interpolate to
# @param[in] alpha how far to interpolate
# @returns The result of the linear interpolation (float)
def lerp(start, end, alpha):
    return (start + alpha * (end - start))


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


## This function for establish dependencies bitween pins
# @param[in] affects_pin this pin affects other pins
# @param[in] affected_pin this pin affected by other pin
def pinAffects(affects_pin, affected_pin):
    affects_pin.affects.append(affected_pin)
    affected_pin.affected_by.append(affects_pin)


## Check for cycle connected nodes
# @param[in] left hand side pin
# @param[in] right hand side pin
# @returns bool
# TODO: remove this, need to find leafs first
# then build recursion stack
def cycle_check(src, dst):
    # allow cycles on execs
    if src.dataType == 'ExecPin' or dst.dataType == 'ExecPin':
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycle_check(start, i):
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


class REGISTER_ENUM(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls):
        Enums.appendEnumInstance(cls)
        return cls


## Used in PyFlow.AbstractGraph.NodeBase.getPinByName for optimization purposes
class PinSelectionGroup(IntEnum):
    Inputs = 0
    Outputs = 1
    BothSides = 2


## Can be used for code generation
class AccessLevel(IntEnum):
    public = 0
    private = 1
    protected = 2


## Determines wheter it is input pin or output.
class PinDirection(IntEnum):
    Input = 0
    Output = 1


## Determines wheter it is callable node or pure.
# Callable node is a node with Exec pins
class NodeTypes(IntEnum):
    Callable = 0
    Pure = 1


@REGISTER_ENUM()
## Direction identifires. Used in [alignSelectedNodes](@ref PyFlow.Core.Widget.GraphWidget.alignSelectedNodes)
class Direction(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

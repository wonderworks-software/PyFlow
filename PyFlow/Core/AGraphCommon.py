"""@file AGraphCommon.py

**AGraphCommon.py** is a common definitions file

this file is imported in almost all others files of the program
"""
import math
import time
from Settings import *
import inspect
from threading import Thread
from functools import wraps
from Queue import Queue
import uuid
import sys
from enum import IntEnum


## determines step for all floating point input widgets
FLOAT_SINGLE_STEP = 0.01
## determines floating precision
FLOAT_DECIMALS = 10
## determines floating minimum value
FLOAT_RANGE_MIN = 0.1 + (-sys.maxint - 1.0)
## determines floating maximum value
FLOAT_RANGE_MAX = sys.maxint + 0.1
## determines int minimum value
INT_RANGE_MIN = -sys.maxint + 0
## determines int maximum value
INT_RANGE_MAX = sys.maxint + 0


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


## Rounding up to sertain value.Used in grid snapping
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
# @param[in] src pin
# @param[in] dst pin
# @returns bool
def cycle_check(src, dst):
    # allow cycles on execs
    if src.dataType == DataTypes.Exec or dst.dataType == DataTypes.Exec:
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


##  Decorator from <a href="https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize">Python decorator library</a>
# @param[in] foo function to memorize
def memoize(foo):
    memo = {}

    @wraps(foo)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = foo(*args)
            memo[args] = rv
            return rv
    return wrapper


## Data types identifires.
class DataTypes(IntEnum):
    Float = 0
    Int = 1
    String = 2
    Bool = 3
    Array = 4
    ## This type represents Execution pins.
    # It doesn't carry any data, but it implements [call](@ref PyFlow.Pins.ExecPin.ExecPin#call) method.
    # Using pins of this type we can control execution flow of graph.
    Exec = 5
    ## Special type of data which represents value passed by reference using [implementNode](@ref PyFlow.Core.FunctionLibrary.implementNode) decorator.
    # For example see [factorial](@ref FunctionLibraries.MathLib.MathLib.factorial) function.
    # Here along with computation results we return additional info, whether function call succeeded or not.
    Reference = 6
    FloatVector3 = 7
    FloatVector4 = 8
    Matrix33 = 9
    Matrix44 = 10
    Quaternion = 11


## Returns string representation of the data type identifier
# See [DataTypes](@ref PyFlow.Core.AGraphCommon.DataTypes)
# @param[in] data type identifier (int)
def getDataTypeName(inValue):
    for name, value in inspect.getmembers(DataTypes):
        if isinstance(value, int):
            if inValue == value:
                return name
    return None


class asynchronous(object):
    def __init__(self, func):
        self.func = func

        def threaded(*args, **kwargs):
            self.queue.put(self.func(*args, **kwargs))

        self.threaded = threaded

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.queue = Queue()
        thread = Thread(target=self.threaded, args=args, kwargs=kwargs)
        thread.start()
        return asynchronous.Result(self.queue, thread)

    class NotYetDoneException(Exception):
        def __init__(self, message):
            self.message = message

    class Result(object):
        def __init__(self, queue, thread):
            self.queue = queue
            self.thread = thread

        def is_done(self):
            return not self.thread.is_alive()

        def get_result(self):
            if not self.is_done():
                raise asynchronous.NotYetDoneException('the call has not yet completed its task')

            if not hasattr(self, 'result'):
                self.result = self.queue.get()

            return self.result


## [Circular buffer](https://en.wikipedia.org/wiki/Circular_buffer) container class.
# Useful for processing streaming data.
class CircularBuffer(object):
    def __init__(self, capacity):
        super(CircularBuffer, self).__init__()
        self._capacity = capacity
        self._ls = []
        self._current = 0

    def _is_full(self):
        return len(self._ls) == self.capacity()

    def append(self, item):
        if self._is_full():
            self._ls[self._current] = item
            self._current = (self._current + 1) % self.capacity()
        else:
            self._ls.append(item)

    def get(self):
        if self._is_full():
            return self._ls[self._current:] + self._ls[:self._current]
        else:
            return self._ls

    def capacity(self):
        return self._capacity


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


## Direction identifires. Used in [alignSelectedNodes](@ref PyFlow.Core.Widget.GraphWidget.alignSelectedNodes)
class Direction(IntEnum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

import math
import time
from Settings import *
import inspect
from threading import Thread
from functools import wraps
from Queue import Queue
import uuid
import sys


FLOAT_SINGLE_STEP = 0.01
FLOAT_DECIMALS = 10
FLOAT_RANGE_MIN = (-sys.maxint - 1.0) + 0.1
FLOAT_RANGE_MAX = sys.maxint + 0.1
INT_RANGE_MIN = -sys.maxint
INT_RANGE_MAX = sys.maxint


def lerp(start, end, alpha):
    return (start + alpha * (end - start))


def getMidPoint(args):
    return [sum(i) / len(i) for i in zip(*args)]


def clamp(n, vmin, vmax):
    return max(min(n, vmax), vmin)


def roundup(x, to):
    return int(math.ceil(x / to)) * to


def pinAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween pins
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


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


def push(start_from):
    '''
    marks dirty all ports from start to the right
    this part of graph will be recomputed every tick
    '''
    if not start_from.affects == []:
        start_from.setDirty()
        for i in start_from.affects:
            i.setDirty()
            push(i)


def getPinColorByType(t):
    if t == DataTypes.Float:
        return Colors.Float
    if t == DataTypes.Int:
        return Colors.Int
    if t == DataTypes.Array:
        return Colors.Array
    if t == DataTypes.Bool:
        return Colors.Bool
    if t == DataTypes.Exec:
        return Colors.Exec
    if t == DataTypes.String:
        return Colors.String
    if t == DataTypes.FloatVector2:
        return Colors.FloatVector2
    if t == DataTypes.FloatVector3:
        return Colors.FloatVector3
    if t == DataTypes.FloatVector4:
        return Colors.FloatVector4


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


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


class DataTypes:
    '''
    Data types identifires.
    '''
    Float = 0
    Int = 1
    String = 2
    Bool = 3
    Array = 4
    Exec = 5
    Reference = 6
    FloatVector3 = 7
    FloatVector4 = 8
    Matrix33 = 9
    Matrix44 = 10
    Quaternion = 11


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


# circular buffer
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


class PinSelectionGroup:
    Inputs = -1
    Outputs = 1
    BothSides = 0


class PinDirection:
    Input = 0
    Output = 1


class NodeTypes:
    Callable = 0
    Pure = 1


class Direction:
    Left = 0
    Right = 1
    Up = 2
    Down = 3

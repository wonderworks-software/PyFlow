'''
common defines, functions and structures
'''
import math
from Settings import *
import inspect
from threading import Thread


FLAG_SYMBOL = "~"


def clamp(n, vmin, vmax):
    return max(min(n, vmax), vmin)


def roundup(x, to):
    return int(math.ceil(x / to)) * to


def pinAffects(affects_port, affected_port):
    '''
    this function for establish dependencies bitween ports
    '''
    affects_port.affects.append(affected_port)
    affected_port.affected_by.append(affects_port)


def calc_multithreaded(ls):
    def compute_executor():
        for n in ls:
            n.compute()
    threads = []
    for n in ls:
        t = Thread(target=compute_executor, name='{0}_thread'.format(n.name))
        threads.append(t)
        t.start()

    [t.join() for t in threads]


def cycle_check(src, dst):

    # allow cycles on execs
    if src.dataType == DataTypes.Exec or dst.dataType == DataTypes.Exec:
        return False

    if src.type == PinTypes.Input:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycle_check(start, i):
            return True
    return False


def findPinsBehind(start_from):
    out = []

    def foo(start_from):
        if not start_from.affected_by == []:
            for p in start_from.affected_by:
                out.append(p)
                foo(p)
    foo(start_from)
    return out


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


def getPortColorByType(t):
    if t == DataTypes.Any:
        return Colors.Any
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


def getDefaultDataValue(dataType):
    if dataType == DataTypes.Float:
        return float()
    if dataType == DataTypes.Int:
        return int()
    if dataType == DataTypes.String:
        return str("none")
    if dataType == DataTypes.Bool:
        return bool()
    if dataType == DataTypes.Array:
        return []
    if dataType == DataTypes.Any:
        return str("none")


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


class DataTypes:
    Float = 0
    Int = 1
    String = 2
    Bool = 3
    Array = 4
    Any = 5
    Exec = 6
    Reference = 7


def getDataTypeName(inValue):
    for name, value in inspect.getmembers(DataTypes):
        if isinstance(value, int):
            if inValue == value:
                return name
    return None


class ObjectTypes(object):
    Pin = 0
    Node = 1
    Graph = 2
    Grouper = 3
    Connection = 4
    NodeName = 5
    SelectionRect = 6
    Scene = 7
    NodeBox = 8


class PinSelectionGroup:
    Inputs = -1
    Outputs = 1
    BothSides = 0


class PinTypes:
    Input = 0
    Output = 1


class NodeTypes:
    Callable = 0
    Pure = 1

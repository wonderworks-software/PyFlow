"""
.. sidebar:: **Common.py**

    **Common.py** is a common definitions file. This file is imported in almost all others files of the program

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


def lerp(start, end, alpha):
    """Performs a linear interpolation

    >>> start + alpha * (end - start)

    :param start: start the value to interpolate from
    :param end: end the value to interpolate to
    :param alpha: alpha how far to interpolate
    :returns: The result of the linear interpolation
    """
    return (start + alpha * (end - start))


def GetRangePct(MinValue, MaxValue, Value):
    """Calculates the percentage along a line from **MinValue** to **MaxValue** that value is.

    :param MinValue: Minimum Value
    :param MaxValue: Maximum Value
    :param Value: Input value
    :returns: The percentage (from 0.0 to 1.0) betwen the two values where input value is
    """
    return (Value - MinValue) / (MaxValue - MinValue)


def sign(x):
    """Returns sign of x. -1 if x is negative, 1 if positive and zero if 0.

    >>> x and (1, -1)[x < 0]
    """
    return x and (1, -1)[x < 0]


def clamp(n, vmin, vmax):
    """Computes the value of the first specified argument clamped to a range defined by the second and third specified arguments

    :param n: input Value
    :param vmin: MiniMum Value
    :param vmax: Maximum Value
    :returns: The clamped value of n
    """
    return max(min(n, vmax), vmin)


def roundup(x, to):
    """Rounding up to sertain value

    >>> roundup(7, 8)
    >>> 8
    >>> roundup(8, 8)
    >>> 8
    >>> roundup(9, 8)
    >>> 16

    :param x: value to round
    :param to: value x will be rounded to
    :returns: rounded value of x
    :rtype: int
    """
    return int(math.ceil(x / to)) * to


currentVersion = Version(sys.version_info.major, sys.version_info.minor, 0)
python32 = Version(3, 2, 0)
if currentVersion <= python32:
    def clearList(list):
        """Clears python list

        :param list:  list to clear
        :type list: list
        :returns: cleared List
        :rtype: list
        """
        del list[:]
else:
    def clearList(list):
        """Clears python list

        :param list:  list to clear
        :type list: list
        :returns: cleared List
        :rtype: list
        """
        list.clear()

def findGoodId(ids):
    """
    Finds good minimum unique int from iterable. Starting from 1

    :param ids: a collection of occupied ids
    :type ids: list|set|tuple
    :returns: Unique Id
    :rtype: int
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
    """Generates function string which then can be compiled and executed

    Example:
    ::

        wrapStringToFunctionDef('test', 'print(a)', {'a': 5})

    Will produce following function:
    ::

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


def cycleCheck(src, dst):
    """Check for cycle connected nodes

    :param src: hand side pin
    :type src: :class:`PyFlow.Core.PinBase`
    :param dst: hand side pin
    :type dst: :class:`PyFlow.Core.PinBase`
    :returns: True if cycle deteted
    :rtype: bool
    """
    if src.direction == PinDirection.Input:
        src, dst = dst, src
    start = src
    if src in dst.affects:
        return True
    for i in dst.affects:
        if cycleCheck(start, i):
            return True
    return False


def arePinsConnected(src, dst):
    """Checks if two pins are connected

    .. note:: Pins can be passed in any order if **src** pin is :py:class:`PyFlow.Core.Common.PinDirection`, they will be swapped

    :param src: left hand side pin
    :type src: :py:class:`PyFlow.Core.PinBase`
    :param dst: right hand side pin
    :type dst: :py:class:`PyFlow.Core.PinBase`
    :returns: True if Pins are connected
    :rtype: bool
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
    """Find all connected Pins to input Pin

    :param pin: Pin to search connected pins
    :type pin: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: Set of connected pins
    :rtype: set(:py:class:`PyFlow.Core.PinBase.PinBase`)
    """
    result = set()
    if pin.direction == PinDirection.Input:
        for lhsPin in pin.affected_by:
            result.add(lhsPin)
    if pin.direction == PinDirection.Output:
        for rhsPin in pin.affects:
            result.add(rhsPin)
    return result


def pinAffects(lhs, rhs):
    """This function for establish dependencies bitween pins

    .. warning:: Used internally, users will hardly need this

    :param lhs: First pin to connect
    :type lhs: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param rhs: Second Pin to connect
    :type rhs: :py:class:`PyFlow.Core.PinBase.PinBase`
    """
    assert(lhs is not rhs), "pin can not affect itself"
    lhs.affects.add(rhs)
    rhs.affected_by.add(lhs)


def canConnectPins(src, dst):
    """**Very important fundamental function, it checks if connection between two pins is possible**

    :param src: Source pin to connect
    :type src: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param dst: Destination pin to connect
    :type dst: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: True if connection can be made, and False if connection is not possible
    :rtype: bool
    """
    if src is None or dst is None:
        return False

    if src.direction == dst.direction:
        return False

    if arePinsConnected(src, dst):
        return False

    if src.direction == PinDirection.Input:
        src, dst = dst, src

    if cycleCheck(src, dst):
        return False

    if src.isExec() and dst.isExec():
        return True

    if not src.isArray() and dst.isArray():
        if dst.optionEnabled(PinOptions.SupportsOnlyArrays) and not (src.canChangeStructure(dst._currStructure, []) or dst.canChangeStructure(src._currStructure, [], selfCheck=False)):
            return False

    if not src.isDict() and dst.isDict():
        if dst.optionEnabled(PinOptions.SupportsOnlyArrays):
            if not (src.canChangeStructure(dst._currStructure, []) or dst.canChangeStructure(src._currStructure, [], selfCheck=False)):
                return False
        elif not src.supportDictElement([], src.optionEnabled(PinOptions.DictElementSupported)) and dst.optionEnabled(PinOptions.SupportsOnlyArrays) and not dst.canChangeStructure(src._currStructure, [], selfCheck=False):
            return False
        else:
            DictElement = src.getDictElementNode([])
            dictNode = dst.getDictNode([])
            nodeFree = False
            if dictNode:
                nodeFree = dictNode.KeyType.checkFree([])
            if DictElement:
                if not DictElement.key.checkFree([]) and not nodeFree:
                    if dst._data.keyType != DictElement.key.dataType:
                        return False

    if src.isArray() and not dst.isArray():
        srcCanChangeStruct = src.canChangeStructure(dst._currStructure, [])
        dstCanCnahgeStruct = dst.canChangeStructure(src._currStructure, [], selfCheck=False)
        if not dst.optionEnabled(PinOptions.ArraySupported) and not (srcCanChangeStruct or dstCanCnahgeStruct):
            return False

    if src.isDict() and not dst.isDict():
        srcCanChangeStruct = src.canChangeStructure(dst._currStructure, [])
        dstCanCnahgeStruct = dst.canChangeStructure(src._currStructure, [], selfCheck=False)
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

    if src.owningNode().graph() is not dst.owningNode().graph():
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
            a = src.dataType == "AnyPin" and not src.canChangeTypeOnConnection([], src.optionEnabled(PinOptions.ChangeTypeOnConnection), [])
            b = dst.canChangeTypeOnConnection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []) and not dst.optionEnabled(PinOptions.AllowAny)
            c = not dst.canChangeTypeOnConnection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []) and not dst.optionEnabled(PinOptions.AllowAny)
            if all([a, b or c]):
                return False
            if not src.isDict() and dst.supportOnlyDictElement([], dst.isDict()) and not (dst.checkFree([], selfCheck=False) and dst.canChangeStructure(src._currStructure, [], selfCheck=False)):
                if not src.supportDictElement([], src.optionEnabled(PinOptions.DictElementSupported)) and dst.supportOnlyDictElement([], dst.isDict()):
                    return False
            return True
        else:
            if all([src.dataType in list(dst.allowedDataTypes([], dst._defaultSupportedDataTypes, selfCheck=dst.optionEnabled(PinOptions.AllowMultipleConnections), defaults=True)) + ["AnyPin"],
                   dst.checkFree([], selfCheck=dst.optionEnabled(PinOptions.AllowMultipleConnections))]):
                return True
            if all([dst.dataType in list(src.allowedDataTypes([], src._defaultSupportedDataTypes, defaults=True)) + ["AnyPin"],
                   src.checkFree([])]):
                return True
        return False

    if src.owningNode == dst.owningNode:
        return False

    return True

def connectPins(src, dst):
    """**Connects two pins**

    This are the rules how pins connect:

    * Input value pins can have one output connection if :py:class:`PyFlow.Core.Common.PinOptions.AllowMultipleConnections` flag is disabled
    * Output value pins can have any number of connections
    * Input execs can have any number of connections
    * Output execs can have only one connection

    :param src: left hand side pin
    :type src: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param dst: right hand side pin
    :type dst: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: True if connected Succesfully
    :rtype: bool
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
    """Connects pins regardless name.

    This function uses pin locations on node. Top most pin have position index 1, pin below - 2 etc.

    :param lhsNode: Left hand side node
    :type lhsNode: :class:`~PyFlow.Core.NodeBase.NodeBase`
    :param lhsOutPinIndex: Out pin position on left hand side node
    :type lhsOutPinIndex: int
    :param rhsNode: Right hand side node
    :type rhsNode: :class:`~PyFlow.Core.NodeBase.NodeBase`
    :param rhsInPinIndex: Out pin position on right hand side node
    :type rhsInPinIndex: int
    """
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

def traverseConstrainedPins(startFrom, callback):
    """Iterate over constrained and connected pins

    Iterates over all constrained chained pins of type :class:`Any <PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin>` and passes pin into callback function. Callback will be executed once for every pin

    :param startFrom: First pin to start Iteration
    :type startFrom: :class:`~PyFlow.Core.PinBase.PinBase`
    :param callback: Functor to execute in each iterated pin.
    :type callback: callback(:class:`~PyFlow.Core.PinBase.PinBase`)
    """
    if not startFrom.isAny():

        return
    traversed = set()

    def worker(pin):
        traversed.add(pin)
        callback(pin)

        if pin.constraint is None:
            nodePins = set()
        else:
            nodePins = set(pin.owningNode().constraints[pin.constraint])

        for connectedPin in getConnectedPins(pin):
            if connectedPin.isAny():
                nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                worker(neighbor)

    worker(startFrom)


def disconnectPins(src, dst):
    """Disconnects two pins

    :param src: left hand side pin
    :type src: :py:class:`~PyFlow.Core.PinBase.PinBase`
    :param dst: right hand side pin
    :type dst: :py:class:`~PyFlow.Core.PinBase.PinBase`
    :returns: True if disconnection succes
    :rtype: bool
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


def push(start_from):
    """Marks dirty all ports from start to the right

    this part of graph will be recomputed every tick

    :param start_from: pin from which recursion begins
    :type start_from: :py:class:`~PyFlow.Core.PinBase.PinBase`
    """
    if not len(start_from.affects) == 0:
        start_from.setDirty()
        for i in start_from.affects:
            i.setDirty()
            push(i)


def extractDigitsFromEndOfString(string):
    """Get digist at end of a string

    Example:

    >>> nums = extractDigitsFromEndOfString("h3ello154")
    >>> print(nums, type(nums))
    >>> 154 <class 'int'>

    :param string: Input numbered string
    :type string: str
    :returns: Numbers in the final of the string
    :rtype: int
    """
    result = re.search('(\d+)$', string)
    if result is not None:
        return int(result.group(0))


def removeDigitsFromEndOfString(string):
    """Delte the numbers at the end of a string

    Similar to :func:`~PyFlow.Core.Common.extractDigitsFromEndOfString`, but removes digits in the end.

    :param string: Input string
    :type string: string
    :returns: Modified string
    :rtype: string
    """
    return re.sub(r'\d+$', '', string)


def getUniqNameFromList(existingNames, name):
    """Create unique name

    Iterates over **existingNames** and extracts the end digits to find a new unique id

    :param existingNames: List of strings where to search for existing indexes
    :type existingNames: list
    :param name: Name to obtain a unique version from
    :type name: str
    :returns: New name non overlapin with any in existingNames
    :rtype: str
    """
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

    :param signal: emitter
    :type signal: :class:`~blinker.base.Signal`
    """
    for receiver in list(signal.receivers.values()):
        if isinstance(receiver, weakref.ref):
            signal.disconnect(receiver())
        else:
            signal.disconnect(receiver)


class SingletonDecorator:
    """Decorator to make class unique, so each time called same object returned
    """

    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


class DictElement(tuple):
    """PyFlow dict element class

    This subclass of python's :class:`tuple` is to represent dict elements to construct typed dicts
    """
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
        return super(DictElement, self).__new__(self, new)


class PFDict(dict):
    """This subclass of python's :class:`dict` implements a key typed dictionary.

    Only defined data types can be used as keys, and only hashable ones as determined by

    >>> isinstance(dataType, collections.Hashable)

    To make a Class Hashable some methods should be implemented:

    Example:
    ::

        class C:
            def __init__(self, x):
                self.x = x
            def __repr__(self):
                return "C({})".format(self.x)
            def __hash__(self):
                return hash(self.x)
            def __eq__(self, other):
                return (self.__class__ == other.__class__ and self.x == other.x)
    """

    def __init__(self, keyType, valueType=None, inpt={}):
        """
        :param keyType: Key dataType
        :param valueType: value dataType, defaults to None
        :type valueType: optional
        :param inpt: Construct from another dict, defaults to {}
        :type inpt: dict, optional
        """
        super(PFDict, self).__init__(inpt)
        self.keyType = keyType
        self.valueType = valueType

    def __setitem__(self, key, item):
        """Reimplements Python Dict __setitem__ to only allow Typed Keys.

        Will throw an Exception if non Valid KeyType
        """
        if type(key) == self.getClassFromType(self.keyType):
            super(PFDict, self).__setitem__(key, item)
        else:
            raise Exception(
                "Valid key should be a {0}".format(self.getClassFromType(self.keyType)))

    def getClassFromType(self, pinType):
        """
        Gets the internal data structure for a defined pin type

        :param pinType: pinType Name
        :type pinType: class or None
        """
        pin = findPinClassByType(pinType)
        if pin:
            pinClass = pin.internalDataStructure()
            return pinClass
        return None


class PinReconnectionPolicy(IntEnum):
    """How to behave if pin has connections and another connection about to be performed.
    """

    DisconnectIfHasConnections = 0  #: Current connection will be broken
    ForbidConnection = 1  #: New connection will be cancelled


class PinOptions(Flag):
    """Used to determine how Pin behaves.

    Apply flags on pin instances.

    .. seealso:: :meth:`~PyFlow.Core.PinBase.PinBase.enableOptions` :meth:`~PyFlow.Core.PinBase.PinBase.disableOptions`
    """

    ArraySupported = auto()  #: Pin can hold array data structure
    DictSupported = auto()  #: Pin can hold dict data structure
    SupportsOnlyArrays = auto()  #: Pin will only support other pins with array data structure

    AllowMultipleConnections = auto()  #: This enables pin to allow more that one input connection. See :func:`~PyFlow.Core.Common.connectPins`

    ChangeTypeOnConnection = auto()  #: Used by :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` to determine if it can change its data type on new connection.
    RenamingEnabled = auto()  #: Determines if pin can be renamed
    Dynamic = auto()  #: Specifies if pin was created dynamically (during program runtime)
    AlwaysPushDirty = auto()  #: Pin will always be seen as dirty (computation needed)
    Storable = auto()  #: Determines if pin data can be stored when pin serialized
    AllowAny = auto()  #: Special flag that allow a pin to be :class:`~PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin`, wich means non typed without been marked as error. By default a :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` need to be initialized with some data type, other defined pin. This flag overrides that. Used in lists and non typed nodes
    DictElementSupported = auto()  #: Dicts are constructed with :class:`DictElement` objects. So dict pins will only allow other dicts until this flag enabled. Used in :class:`~PyFlow.Packages.PyFlowBase.Nodes.makeDict` node


class PinStructure(IntEnum):
    """Structure of Pins

    Used for determine Pin Structure Type
    This represents the data structures a pin can hold.
    """

    Single = 0  #: Single data structure
    Array = 1  #: Python list structure, represented as arrays -> typed and lists -> non typed
    Dict = 2  #: :py:class:`PFDict` structure, is basically a rey typed python dict
    Multi = 3  #: This means it can became any of the previous ones on conection/user action


def findStructFromValue(value):
    """Finds :class:`~PyFlow.Core.Common.PinStructure` from value

    :param value: input value to find structure.
    :returns: Structure Type for input value
    :rtype: :class:`~PyFlow.Core.Common.PinStructure`
    """

    if isinstance(value, list):
        return PinStructure.Array
    if isinstance(value, dict):
        return PinStructure.Dict
    return PinStructure.Single


class PinSelectionGroup(IntEnum):
    """Used in :meth:`~PyFlow.Core.NodeBase.NodeBase.getPinSG` for optimization purposes
    """

    Inputs = 0  #: Input pins
    Outputs = 1  #: Outputs pins
    BothSides = 2  #: Both sides pins


class AccessLevel(IntEnum):
    """Can be used for code generation
    """

    public = 0  #: public
    private = 1  #: private
    protected = 2  #: protected


class PinDirection(IntEnum):
    """Determines whether it is input pin or output
    """

    Input = 0  #: Left side pins
    Output = 1  #: Right side pins


class NodeTypes(IntEnum):
    """Determines whether it is callable node or pure
    """

    Callable = 0  #: Callable node is a node with exec pins
    Pure = 1  #: Normal nodes


class Direction(IntEnum):
    """ Direction identifiers
    """

    Left = 0  #: Left
    Right = 1  #: Right
    Up = 2  #: Up
    Down = 3  #: Down

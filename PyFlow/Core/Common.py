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


def lerp(start, end, alpha):
    """Performs a linear interpolation

    start + alpha * (end - start)
    
    :param start: start the value to interpolate from
    :param end: end the value to interpolate to
    :param alpha: alpha how far to interpolate
    :returns: The result of the linear interpolation 
    """
    return (start + alpha * (end - start))


## 
def GetRangePct(MinValue, MaxValue, Value):
    """Calculates the percentage along a line from MinValue to MaxValue that Value is.
    
    :param MinValue: Minimum Value
    :param MaxValue: Maximum Value
    :param Value: [description]
    :returns: The percentage betwen the two values where input value is
    """
    return (Value - MinValue) / (MaxValue - MinValue)


def sign(x):
    """    
    x and (1, -1)[x < 0]
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
    """Rounding up to sertain value. Used in grid snapping
    
    int(math.ceil(x / to)) * to
    :param x: value to round
    :param to: value x will be rounded to
    :returns: rounded value of x
    :rtype: {int}
    """
    return int(math.ceil(x / to)) * to


currentVersion = Version(sys.version_info.major, sys.version_info.minor, 0)
python32 = Version(3, 2, 0)
if currentVersion <= python32:
    def clearList(list):
        """Clearing a list in python previous to 3.2 is not possible with list.clear()
        
        :param list:  list to clear
        :type list: list
        :returns: cleared List
        :rtype: list
        """
        del list[:]
else:
    def clearList(list):
        """Clearing a list in python previous to 3.2 is not possible with list.clear()
        
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
    :type ids: {list|set|tuple}
    :returns: Unique Id
    :rtype: {int}
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
    Example::
        wrapStringToFunctionDef('test', 'print(a)', {'a': 5})
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


def cycle_check(src, dst):
    """[summary]
    
    Check for cycle connected nodes
    :param src: hand side pin
    :type src: :py:class:`PyFlow.Core.PiBase`
    :param dst: hand side pin
    :type dst: :py:class:`PyFlow.Core.PiBase`
    :returns: True if is cycle
    :rtype: {bool}
    """
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
    """    
    Checks if two pins are connected
    :param src: left hand side pin
    :type src: :py:class:`PyFlow.Core.PiBase`
    :param dst: right hand side pin
    :type dst: :py:class:`PyFlow.Core.PiBase`
    :returns: True if Pins are connected
    :rtype: {bool}
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

    :param pin: Pin to search Connected Pins
    :type pin: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: List of connected Pins
    :rtype: {set(:py:class:`PyFlow.Core.PinBase.PinBase`)}
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
    """ This function for establish dependencies bitween pins
    
    :param lhs: First Pin to connect
    :type lhs: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param rhs: Second Pin to connect
    :type rhs: :py:class:`PyFlow.Core.PinBase.PinBase`
    """
    assert(lhs is not rhs), "pin can not affect itself"
    lhs.affects.add(rhs)
    rhs.affected_by.add(lhs)


def canConnectPins(src, dst):
    """** Base function called each time a new connection is tryied **
    
    :param src: Source Pin To connect
    :type src: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param dst: Destination Pin to connect
    :type dst: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: True if connection can be made, and False if connection is not possible
    :rtype: {bool}
    """
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
        if dst.optionEnabled(PinOptions.SupportsOnlyArrays):
            if not (src.canChangeStructure(dst._currStructure, []) or dst.canChangeStructure(src._currStructure, [], selfChek=False)):
                return False
        elif not src.supportDictElement([], src.optionEnabled(PinOptions.DictElementSuported)) and dst.optionEnabled(PinOptions.SupportsOnlyArrays) and not dst.canChangeStructure(src._currStructure, [], selfChek=False):
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
            a = src.dataType == "AnyPin" and not src.canChangeTypeOnConection([], src.optionEnabled(PinOptions.ChangeTypeOnConnection), [])
            b = dst.canChangeTypeOnConection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []) and not dst.optionEnabled(PinOptions.AllowAny)
            c = not dst.canChangeTypeOnConection([], dst.optionEnabled(PinOptions.ChangeTypeOnConnection), []) and not dst.optionEnabled(PinOptions.AllowAny)
            if all([a,b or c]):
                return False
            if not src.isDict() and dst.supportOnlyDictElement([],dst.isDict()) and not (dst.checkFree([],selfChek=False) and dst.canChangeStructure(src._currStructure, [], selfChek=False)):
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
    """**Connects two pins**
    
    Input value pins can have one output connection if `AllowMultipleConnections` flag is disabled
    Output value pins can have any number of connections
    Input execs can have any number of connections
    Output execs can have only one connection
    :param src: left hand side pin
    :type src: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param dst: right hand side pin
    :type dst: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: True if connected Succesfully
    :rtype: {bool}
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

def traverseConstrainedPins(startFrom, callback):
    """**Iterate Over Constrained And Conected Pins**
    
    Iterates over all constrained chained pins of type `Any` and passes pin into callback function. Callback will be executed once for every pin
    :param startFrom: First Pin to start Iteration
    :type startFrom: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param callback: Function to Execute in each iterated Pin
    :type callback: function
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
    """**Disconnects two pins**
    
    [description]
    :param src: left hand side pin
    :type src: :py:class:`PyFlow.Core.PinBase.PinBase`
    :param dst: right hand side pin
    :type dst: :py:class:`PyFlow.Core.PinBase.PinBase`
    :returns: True if disconnection succes
    :rtype: {bool}
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
    """marks dirty all ports from start to the right
    
    this part of graph will be recomputed every tick
    :param start_from: pin from which recursion begins
    :type start_from: :py:class:`PyFlow.Core.PinBase.PinBase`
    """
    if not len(start_from.affects) == 0:
        start_from.setDirty()
        for i in start_from.affects:
            i.setDirty()
            push(i)


def extractDigitsFromEndOfString(string):
    """Get Digist at end of a String
    
    :param string: Input Numbered String
    :type string: string
    :returns: Numbers in the final of the string
    :rtype: {int}
    """
    result = re.search('(\d+)$', string)
    if result is not None:
        return int(result.group(0))


def removeDigitsFromEndOfString(string):
    """Delte the numbers at the end of a String
    
    :param string: Input Numbered String
    :type string: string
    :returns: Cleared String
    :rtype: {string}
    """
    return re.sub(r'\d+$', '', string)


def getUniqNameFromList(existingNames, name):
    """**Create Unique Name**
    
    Iterates over existingNames and extracts the end digists to find a new unique id
    :param existingNames: List of String where to search for existing indexes
    :type existingNames: list
    :param name: Name to obtain a unique version from
    :type name: string
    :returns: New name non overlapin with any in existingNames
    :rtype: {string}
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
    """**Disconnects all receivers**
    
    [description]
    :param signal: blinker Signal class
    :type signal: Signal
    """
    for receiver in list(signal.receivers.values()):
        if isinstance(receiver, weakref.ref):
            signal.disconnect(receiver())
        else:
            signal.disconnect(receiver)


class SingletonDecorator:
    """**Decorator to make Class unique, so each time called same Object returned**
    """
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


class dictElement(tuple):
    """**PyFlow Dict Element Class**
    
    This SubClass of Python tuple is to represent DictElements inEditor to construct Typed Dicts
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
        return super(dictElement, self).__new__(self, new)


class pyf_dict(dict):
    """**PyFlow Dict Class**
    
    This SubClass of Python dict implements a key Typed dictionary.
    Only defined Datatypes can be used as keys, and only Hashable ones as determined by isinstance(dataType, collections.Hashable)

    To make a Class Hashable some methods should be implemented:
    Example::
        class C:
            def __init__(self, x):
                self.x = x
            def __repr__(self):
                return f"C({self.x})"
            def __hash__(self):
                return hash(self.x)
            def __eq__(self, other):
                return (self.__class__ == other.__class__ and self.x == other.x )        
    """
    def __init__(self, keyType, valueType=None, inpt={}):
        """        
        :param keyType: Key dataType
        :param valueType: value dataType, defaults to None
        :type valueType: optional
        :param inpt: Construct from another dict, defaults to {}
        :type inpt: dict, optional
        """
        super(pyf_dict, self).__init__(inpt)
        self.keyType = keyType
        self.valueType = valueType

    def __setitem__(self, key, item):
        """Reimplements Python Dict __setitem__ to only allow Typed Keys.

        Will throw an Exception if non Valid KeyType
        """
        if type(key) == self.getClassFromType(self.keyType):
            super(pyf_dict, self).__setitem__(key, item)
        else:
            raise Exception(
                "Valid key should be a {0}".format(self.getClassFromType(self.keyType)))

    def getClassFromType(self, pinType):
        """        
        Gets the internalDataStructure for a defined pinType
        :param pinType: pinType Name
        :type pinType: string
        """
        pin = findPinClassByType(pinType)
        if pin:
            pinClass = pin.internalDataStructure()
            return pinClass
        return None

class PinReconnectionPolicy(IntEnum):
    DisconnectIfHasConnections = 0
    ForbidConnection = 1


class PinOptions(Flag):
    """**Pin Settings**
    
    used to determine how Pin behaves.
    This is intended to be defined not in Pin Class , but per each defined node.

    :ArraySupported: Pin can hold Array Data Structure.
    :DictSupported: Pin can hold Dict Data Structure.
    :SupportsOnlyArrays: Pin will only support oher Pins with Array Data Structure.
    :AllowMultipleConnections: This enable Pin to allow more that one input Connection. 
                                     By default Pins allows only one input conection and infinite outputs for value Pins,
                                     and infinite inputs and only one  output connection for Execution Pins.
    :ChangeTypeOnConnection: Used by :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` to determine if it can change its dataType on new Connection.
    :RenamingEnabled: Determines if Pin can be renamed inEditor.
    :Dynamic: Especifies if Pin was created dynamically inEditor, Used by Nodes wthat allow user to create Pins in the node.
    :AlwaysPushDirty: Pin will always be seen as Dirty (computation needed)
    :Storable: Determines if Pin data can be stored when graph saved.
    :AllowAny: Special Flag that allow a Pin to be :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin`, wich means nonTyped without been marked as error.
                    By default a :py:class:`PyFlow.Packages.PyFlowBase.Pins.AnyPin.AnyPin` Pin need to be initialized with some DataType, other defined Pin.
                    This flag overrides that. Used in Lists and nonTyped Nodes
    :DictElementSuported: Dicts are constructed inEditor with :py:class:`dictElement` objects. So Dict Pins will only allow other Dicts until this flag enabled,
                                Used in makeDict node.
    """
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

class PinStructure(IntEnum):
    """**Structure of Pins**
    
    Used for determine Pin Structure Type
    This represents the data structures a pin can hold.

    :Single: Single data structure
    :Array: Python List structure, In editor represented as Arrays -> Typed and Lists -> nonTyped
    :Dict: :py:class:`pyf_dict` structure, is basically a KeyTyped Python Dict
    :Multi: This means it can became any of the previous Ones on conection/user action
    """
    Single = 0
    Array = 1
    Dict = 2
    Multi = 3

def findStructFromValue(value):
    """**Finds PinStructure from value**

    :param value: input value to find structure.
    :returns: Structure Type for input value
    :rtype: {py:class:`PinStructure`}
    """
    if isinstance(value, list):
        return PinStructure.Array
    if isinstance(value, dict):
        return PinStructure.Dict
    return PinStructure.Single

class PinSelectionGroup(IntEnum):
    """Used in :py:func:`PyFlow.AbstractGraph.NodeBase.getPin` for optimization purposes

    :Inputs: Input Pins
    :Outputs: Outputs Pins
    :BothSides: BothSides Pins
    """
    Inputs = 0
    Outputs = 1
    BothSides = 2

class AccessLevel(IntEnum):
    """Can be used for code generation

    :public:  
    :private:
    :protected:
    """
    public = 0
    private = 1
    protected = 2

class PinDirection(IntEnum):
    """Determines whether it is input pin or output.

    :Input: Inputs, left side Pins
    :Output: Outpus,right side Pins
    """
    Input = 0
    Output = 1

class NodeTypes(IntEnum):
    """Determines whether it is callable node or pure.

    :Callable:  Callable node is a node with Exec pins.
    :Pure:  Normal Nodes.
    """
    Callable = 0
    Pure = 1

class Direction(IntEnum):
    """ Direction identifiers. Used in :py:func:`PyFlow.Core.Widget.GraphWidget.alignSelectedNodes`

    :Left:
    :Right:
    :Up:
    :Down:
    """
    Left = 0
    Right = 1
    Up = 2
    Down = 3

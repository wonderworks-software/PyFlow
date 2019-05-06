from blinker import Signal
import uuid
from copy import deepcopy
import weakref

from PyFlow.Core.Interfaces import IPin
from PyFlow.Core.Common import *
from PyFlow import getPinDefaultValueByType


class PinBase(IPin):
    _packageName = ""

    def __init__(self, name, owningNode, direction, userStructClass=None):
        super(PinBase, self).__init__()
        # signals
        self.serializationHook = Signal()
        self.onPinConnected = Signal(object)
        self.onPinDisconnected = Signal(object)
        self.nameChanged = Signal(str)
        self.killed = Signal()
        self.onExecute = Signal(object)

        self._uid = uuid.uuid4()
        self._userStructClass = userStructClass
        self._data = None
        self._defaultValue = None
        ## This flag for lazy evaluation
        # @sa @ref PinBase::getData
        self.dirty = True
        ## List of pins this pin connected to
        self.affects = set()
        ## List of pins connected to this pin
        self.affected_by = set()
        ## Access to the node
        self.owningNode = weakref.ref(owningNode)

        self.name = name
        ## Defines is this input pin or output
        self.direction = direction
        ## For rand int node and stuff like that
        self._alwaysPushDirty = False
        ## Can be renamed or not (for switch on string node)
        self._renamingEnabled = False
        ## For example sequence nodes output execs are dynamically created and can be deleted from node as well
        self._dynamic = False

        self._allowMultipleConnections = False

        # gui class weak ref
        self._wrapper = None
        # Constraint ports
        self.constraint = None
        self._isAny = False

        self._isList = False
        self.listSupported = False
        self.supportsOnlyList = False

    def setAllowMultipleConnections(self, bAllow):
        self._allowMultipleConnections = bAllow

    def isAllowMultiConnection(self):
        return self._allowMultipleConnections

    def isAny(self):
        return self._isAny

    @property
    def packageName(self):
        return self._packageName

    @property
    def linkedTo(self):
        # store connection from out pins only
        # from left hand side to right hand side
        result = set()
        if self.direction == PinDirection.Output:
            for i in self.affects:
                result.add(i.getName())
        return result

    def __repr__(self):
        return "[{0}:{1}:{2}:{3}]".format(self.dataType, self.getName(), self.dirty, self.currentData())

    def isExec(self):
        return False

    def setAsList(self, bIsList):
        self._isList = bool(bIsList)
        if bIsList:
            self._data = []

    def isList(self):
        return self._isList

    @staticmethod
    def IsValuePin():
        return True

    def setWrapper(self, wrapper):
        if self._wrapper is None:
            self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        return self._wrapper

    def setRenamingEnabled(self, bEnabled):
        self._renamingEnabled = bEnabled

    def renamingEnabled(self):
        return self._renamingEnabled

    def setDynamic(self, bDynamic):
        self._dynamic = bDynamic

    def isDynamic(self):
        return self._dynamic

    def isAlwaysPushDirty(self):
        return self._alwaysPushDirty

    def setAlwaysPushDirty(self, bValue=False):
        assert(isinstance(bValue, bool))
        self._alwaysPushDirty = bValue

    # ISerializable interface
    def serialize(self):

        uidString = str(self.uid)

        data = {
            'name': self.name,
            'fullName': self.getName(),
            'dataType': self.__class__.__name__,
            'direction': int(self.direction),
            'value': self.currentData(),
            'uuid': uidString,
            'bDirty': self.dirty,
            'dynamic': self.isDynamic(),
            'renamingEnabled': self.renamingEnabled(),
            'alwaysPushDirty': self._alwaysPushDirty,
            'linkedTo': list(self.linkedTo)
        }

        # Wrapper class can subscribe to this signal and return
        # UI specific data which will be considered on serialization.
        # Blinker returns a tuple (receiver, return val)
        wrapperData = self.serializationHook.send(self)
        if wrapperData is not None:
            if len(wrapperData) > 0:
                # We take return value from one wrapper
                data['wrapper'] = wrapperData[0][1]
        return data

    # IItemBase interface

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if not value == self._uid:
            self._uid = value

    def setName(self, name, force=False):
        if not force:
            if not self.renamingEnabled():
                return False
        if name == self.name:
            return False
        self.name = self.owningNode().getUniqPinName(name)
        self.nameChanged.send(self.name)
        return True

    def getName(self):
        return self.owningNode().name + '.' + self.name

    # IPin interface

    ## This used by node box to suggest nodes by type
    @staticmethod
    def pinDataTypeHint():
        return None

    @staticmethod
    def supportedDataTypes():
        return ()

    def defaultValue(self):
        if self.isList():
            return []
        else:
            return self._defaultValue

    # TODO: Move this to separate class (e.g. ExecutionEngine) with PIMPL
    ## retrieving the data
    def getData(self):
        if self.direction == PinDirection.Output:
            if self.dirty:
                self.owningNode().compute()
            self.setClean()
            return self.currentData()
        if self.direction == PinDirection.Input:
            if not self.dirty:
                return self.currentData()
            if self.dirty or self.owningNode().bCallable:
                connectedOutputs = [i for i in self.affected_by if i.direction == PinDirection.Output]
                if len(connectedOutputs) == 1:
                    compute_order = self.owningNode().graph().getEvaluationOrder(connectedOutputs[0].owningNode())
                    # call from left to right
                    for layer in reversed(sorted([i for i in compute_order.keys()])):
                        for node in compute_order[layer]:
                            node.compute()
                    self.setClean()
                    return self.currentData()
                else:
                    self.setClean()
                    return self.currentData()

    ## Setting the data
    def setData(self, data):
        self.setClean()
        self._data = data
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i._data = self.currentData()
                i.setClean()
        if self.direction == PinDirection.Input or self._alwaysPushDirty:
            push(self)

    ## Calling execution pin
    def call(self, *args, **kwargs):
        self.onExecute.send(*args, **kwargs)

    def disconnectAll(self):
        # if input pin
        # 1) loop connected output pins of left connected node
        # 2) call events
        # 3) remove self from other's affection list
        # clear affected_by list
        if self.direction == PinDirection.Input:
            for o in list(self.affected_by):
                disconnectPins(self, o)
            self.affected_by.clear()

        # if output pin
        # 1) loop connected input pins of right connected node
        # 2) call events
        # 3) remove self from other's affection list
        # clear affects list
        if self.direction == PinDirection.Output:
            for i in list(self.affects):
                disconnectPins(self, i)
            self.affects.clear()

    ## Describes, what data type is this pin.
    @property
    def dataType(self):
        return self.__class__.__name__

    def isUserStruct(self):
        return self._userStructClass is not None

    def getUserStruct(self):
        return self._userStructClass

    def setUserStruct(self, inStruct):
        self._userStructClass = inStruct

    # PinBase methods

    def kill(self, *args, **kwargs):
        self.disconnectAll()
        if self in self.owningNode().pins:
            self.owningNode().pins.remove(self)
        self.killed.send()
        clearSignal(self.killed)

    def currentData(self):
        if self._data is None:
            return self._defaultValue
        return self._data

    def pinConnected(self, other):
        self.onPinConnected.send(other)
        push(self)

    def pinDisconnected(self, other):
        self.onPinDisconnected.send(other)
        if self.direction == PinDirection.Output:
            otherPinName = other.getName()
        push(other)

    def setClean(self):
        self.dirty = False
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i.dirty = False

    def hasConnections(self):
        numConnections = 0
        if self.direction == PinDirection.Input:
            numConnections += len(self.affected_by)
        elif self.direction == PinDirection.Output:
            numConnections += len(self.affects)
        return numConnections > 0

    def setDirty(self):
        if self.isExec():
            return
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def setDefaultValue(self, val):
        # In python, all user-defined classes are mutable
        # So make sure to store separate copy of value
        # For example if this is a Matrix, default value will be changed each time data has been set in original Matrix
        self._defaultValue = deepcopy(val)

    def updateConstraint(self, constraint):
        self.constraint = constraint
        if constraint in self.owningNode().constraints:
            self.owningNode().constraints[constraint].append(self)
        else:
            self.owningNode().constraints[constraint] = [self]

import uuid
from copy import deepcopy
import weakref

from PyFlow.Core.Interfaces import IPin
from PyFlow.Core.AGraphCommon import *


class PinBase(IPin):
    def __init__(self, name, owningNode, dataType, direction, userStructClass=None):
        super(PinBase, self).__init__()
        self._uid = uuid.uuid4()
        self._dataType = None
        self._userStructClass = userStructClass
        self._data = None
        self._defaultValue = None
        ## This flag for lazy evaluation
        # @sa @ref PinBase::getData
        self.dirty = True
        self._connected = False
        ## List of pins this pin connected to
        self.affects = []
        ## Lsit of pins connected to this pin
        self.affected_by = []
        ## List of connections
        self.edge_list = []
        ## Access to the node
        if owningNode != None:
            self.owningNode = weakref.ref(owningNode)

        self.name = name
        self.dataType = dataType
        ## Defines is this input pin or output
        self.direction = direction
        ## For rand int node
        self._alwaysPushDirty = False
        ## Can be renamed or not (for switch on string node)
        self._renamingEnabled = False
        ## For examle sequence nodes output execs are dynamically created and can be deleted from node as well
        self._dynamic = False

        # gui class weak ref
        self._wrapper = None
        # Constraint ports
        self.constraint = None
        self.isAny = False

    @staticmethod
    def IsValuePin():
        return True

    def setWrapper(self, wrapper):
        self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        return self._wrapper

    def setRenamingEnabled(self, bEnabled):
        self._renamingEnabled = bEnabled

    def canBeRenamed(self):
        return self._renamingEnabled

    def setDynamic(self, bDynamic):
        self._dynamic = bDynamic

    def isDynamic(self):
        return self._dynamic

    def setAlwaysPushDirty(self, bValue=False):
        assert(isinstance(bValue, bool))
        self._alwaysPushDirty = bValue

    # ISerializable interface
    def serialize(self):
        data = {'name': self.name,
                'dataType': self.dataType,
                'direction': int(self.direction),
                'value': self.currentData(),
                'uuid': str(self.uid),
                'bDirty': self.dirty
                }
        return data

    @staticmethod
    def deserialize(owningNode, jsonData):
        pass

    # IItemBase interface

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self.owningNode().graph().pins[value] = self.owningNode().graph().pins.pop(self._uid)
        self._uid = value

    def setName(self, name):
        oldName = self.name
        self.name = name.replace(" ", "_")
        if self.direction == PinDirection.Input:
            self.owningNode().namePinInputsMap[self.name] = self.owningNode().namePinInputsMap.pop(oldName)
        if self.direction == PinDirection.Output:
            self.owningNode().namePinOutputsMap[self.name] = self.owningNode().namePinOutputsMap.pop(oldName)

    def getName(self):
        return self.owningNode().name + '.' + self.name

    # IPin interface

    ## This used by node box to suggest nodes by type
    @staticmethod
    def pinDataTypeHint():
        return None

    def supportedDataTypes(self):
        return (self.dataType,)

    def defaultValue(self):
        return self._defaultValue

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
                out = [i for i in self.affected_by if i.direction == PinDirection.Output]
                if not out == []:
                    compute_order = self.owningNode().graph().getEvaluationOrder(out[0].owningNode())
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
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i._data = self.currentData()
                i.setClean()
        if self.direction == PinDirection.Input or self._alwaysPushDirty:
            push(self)

    ## Calling execution pin
    def call(self):
        pass

    def disconnectAll(self):
        trash = []
        for e in self.edge_list:
            if self.uid == e.destination().uid:
                trash.append(e)
            if self.uid == e.source().uid:
                trash.append(e)
        return trash

    ## Describes, what data type is this pin.
    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = value

    def isUserStruct(self):
        return self._userStructClass is not None

    def getUserStruct(self):
        return self._userStructClass

    def setUserStruct(self, inStruct):
        self._userStructClass = inStruct

    # PinBase methods

    def kill(self):
        if self.direction == PinDirection.Input and self.uid in self.owningNode().inputs:
            self.owningNode().inputs.pop(self.uid)
            self.owningNode().namePinInputsMap.pop(self.name)
        if self.direction == PinDirection.Output and self.uid in self.owningNode().outputs:
            self.owningNode().outputs.pop(self.uid)
            self.owningNode().namePinOutputsMap.pop(self.name)
        if self.uid in self.owningNode().graph().pins:
            self.owningNode().graph().pins.pop(self.uid)

    def currentData(self):
        if self._data is None:
            return self._defaultValue
        return self._data

    def pinConnected(self, other):
        self._connected = True

    def pinDisconnected(self, other):
        if not self.hasConnections():
            self._connected = False

    def setClean(self):
        self.dirty = False
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i.dirty = False

    def hasConnections(self):
        if len(self.edge_list) == 0:
            return False
        else:
            return True

    def setDirty(self):
        if self.dataType == 'ExecPin':
            return
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def setDefaultValue(self, val):
        # In python, all user-defined classes are mutable
        # So make sure to store sepatrate copy of value
        # For example if this is a Matrix, default value will be changed each time data has been set in original Matrix
        self._defaultValue = deepcopy(val)

    def updateConstraint(self,constraint):
        self.constraint = constraint
        if self.owningNode()._Constraints.has_key(constraint):
            self.owningNode()._Constraints[constraint].append(self)
        else:
            self.owningNode()._Constraints[constraint] = [self]
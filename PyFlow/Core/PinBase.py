from blinker import Signal
import uuid
from copy import deepcopy
import weakref
import json

from PyFlow.Core.Interfaces import IPin
from PyFlow.Core.Common import *
from PyFlow import getPinDefaultValueByType


class PinBase(IPin):
    _packageName = ""

    def __init__(self, name, owningNode, direction):
        super(PinBase, self).__init__()
        # signals
        self.serializationHook = Signal()
        self.onPinConnected = Signal(object)
        self.onPinDisconnected = Signal(object)
        self.nameChanged = Signal(str)
        self.killed = Signal()
        self.onExecute = Signal(object)
        self.containerTypeChanged = Signal()
        ## Access to the node
        self.owningNode = weakref.ref(owningNode)
        self._uid = uuid.uuid4()
        self._data = None
        self._defaultValue = None
        # What to do if connect with busy pin. Used when AllowMultipleConnections flag is disabled
        self.reconnectionPolicy = PinReconnectionPolicy.DisconnectIfHasConnections
        ## This flag for lazy evaluation
        self.dirty = True
        ## List of pins this pin connected to
        self.affects = set()
        ## List of pins connected to this pin
        self.affected_by = set()

        self.name = name
        ## Defines is this input pin or output
        self.direction = direction

        # gui class weak ref
        self._wrapper = None
        # Constraint ports
        self.constraint = None
        self.structConstraint = None

        # Flags
        self._flags = PinOptions.Storable
        self._origFlags = self._flags
        self._structure = PinStructure.Single
        self._currStructure = self._structure
        self._structFree = True
        self._free = False
        self._isAny = False
        self._isArray = False
        self._alwaysList = False
        self.changeTypeOnConnection = False
        self._defaultSupportedDataTypes = self._supportedDataTypes = self.supportedDataTypes()

    def enableOptions(self, *options):
        for option in options:
            self._flags = self._flags | option
            self._origFlags = self._flags

    def disableOptions(self, *options):
        for option in options:
            self._flags = self._flags & ~option
            self._origFlags = self._flags

    def optionEnabled(self, option):
        return bool(self._flags & option)

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

    def initAsArray(self,bIsList):
        """Sets this pins to be a list always"""
        bIsList = bool(bIsList)
        self._alwaysList = bIsList
        self.setAsArray(bIsList)

    def setAsArray(self, bIsList):
        """Sets this pin to be a list.

        Every registered pin can hold a list of values instead of single one. List pins can be connected
        only with another list pins by default. This behavior can be changed by disabling `PinOptions.SupportsOnlyArrays` option.

        Value pins can be connected only with value pins if option `PinOptions.v` is not enabled.

        By default input value pin can have only one connection, this also can be modified by enabling `PinOptions.AllowMultipleConnections` flag.

        Args:

            bIsList (bool): list or not
        """
        bIsList = bool(bIsList)
        if self._isArray == bIsList:
            return

        self._isArray = bIsList
        if bIsList:
            self._data = []
            # list pins supports only lists by default
            self.enableOptions(PinOptions.SupportsOnlyArrays)
            #self.changeTypeOnConnection = True
            self._currStructure = PinStructure.Array
        else:
            self._flags = self._origFlags
            self._currStructure = self._structure

        self.containerTypeChanged.send()

    def isArray(self):
        return self._isArray

    @staticmethod
    def IsValuePin():
        return True

    def setWrapper(self, wrapper):
        if self._wrapper is None:
            self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        return self._wrapper

    # ISerializable interface
    def serialize(self):

        storable = self.optionEnabled(PinOptions.Storable)

        serializedData = None
        if storable:
            serializedData = json.dumps(self.currentData(), cls=self.jsonEncoderClass())
        else:
            serializedData = json.dumps(self.defaultValue(), cls=self.jsonEncoderClass())

        data = {
            'name': self.name,
            'fullName': self.getName(),
            'dataType': self.__class__.__name__,
            'direction': int(self.direction),
            'value': serializedData,
            'uuid': str(self.uid),
            'bDirty': self.dirty,
            'linkedTo': list(self.linkedTo),
            'options': [i.value for i in PinOptions if self.optionEnabled(i)],
            'changeType':self.changeTypeOnConnection
        }

        # Wrapper class can subscribe to this signal and return
        # UI specific data which will be considered on serialization
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
            if not self.optionEnabled(PinOptions.RenamingEnabled):
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

    def allowedDataTypes(self, checked=[], dataTypes=[],selfChek=True,defaults=False):
        return list(self.supportedDataTypes())

    def checkFree(self, checked=[], selfChek=True):
        return False
        
    def defaultValue(self):
        if self.isArray():
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
        if self.direction == PinDirection.Input or self.optionEnabled(PinOptions.AlwaysPushDirty):
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

    ## Describes, what structure of data is this pin.
    @property
    def structureType(self):
        return self._structure

    @structureType.setter
    def structureType(self,structure):
        self._structure = structure
        self._currStructure = structure

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

    def aboutToConnect(self,other):
        self.changeStructure(other._currStructure,other._flags)  
        self.onPinConnected.send(other)  

    def changeStructure(self,newStruct,flags,init=False):
        if self.structureType == PinStructure.Multi and self._currStructure != newStruct:
            if newStruct == PinStructure.Array and not (self.optionEnabled(PinOptions.ArraySupported) or init):
                return
            else:
                free = self.canChangeStructure(newStruct,[])
                print self,free
                if free :
                    self._structFree = False
                    if not init:
                        self.setAsArray(newStruct==PinStructure.Array)
                    else:
                        self.initAsArray(newStruct==PinStructure.Array)
                    self._currStructure = newStruct
                    self._flags = flags
                    if newStruct == PinStructure.Single :
                        self.disableOptions(PinOptions.ArraySupported)
                        self.disableOptions(PinOptions.SupportsOnlyArrays)
                    else :
                        self.enableOptions(PinOptions.ArraySupported)
                    
                    traversed = set()
                    traversed.add(self)   
                    self.updateConstrainedPins(traversed,self.isArray(),self._flags,connecting=True) 

    def pinConnected(self, other):
        push(self)

    def updateConstrainedPins(self,traversed,array,flags,connecting=False):
        nodePins = set()
        if self.structConstraint is not None:
            nodePins = set(self.owningNode().structConstraints[self.structConstraint])
        for connectedPin in getConnectedPins(self):
            if connectedPin.structureType == PinStructure.Multi:
                if connectedPin.canChangeStructure(self._currStructure):
                    nodePins.add(connectedPin)    
        for neighbor in nodePins:
            if neighbor not in traversed:
                neighbor.setAsArray(array)
                neighbor._flags = flags
                if connecting:
                    neighbor._currStructure = self._currStructure
                else:
                    neighbor._currStructure = neighbor._structure
                    neighbor._data = neighbor.defaultValue()
                traversed.add(neighbor) 
                neighbor.updateConstrainedPins(traversed,array,flags,connecting=connecting)

    def pinDisconnected(self, other):
        self.onPinDisconnected.send(other)
        if self.direction == PinDirection.Output:
            otherPinName = other.getName()
        """
        free = self.canChangeStructure(self._structure,[])
        if free:
            self._structFree = True
            self.setAsArray(False)
            self._flags = self._origFlags
            self._data = self.defaultValue()
            traversed = set()
            traversed.add(self)   
            self.updateConstrainedPins(traversed,False,self._flags)  
        """            
        push(other)

    def canChangeStructure(self,newStruct, checked=[], selfChek=True):
        # if self.constraint is None:
        if self.structConstraint is None and self.structureType == PinStructure.Multi:#(newStruct !=PinStructure.Array and self.structureType == PinStructure.Array and self.optionEnabled(PinOptions.AllowMultipleConnections))
            return True
        elif self.structureType != PinStructure.Multi :
            return False
        else:
            con = []
            if selfChek:
                free = not self.hasConnections()
                if not free:
                    for c in getConnectedPins(self):
                        if c not in checked:
                            con.append(c)
            else:
                free = True
                checked.append(self)
            free = True
            for port in self.owningNode().structConstraints[self.structConstraint] + con:
                if port not in checked:
                    checked.append(port)
                    if self.owningNode() == port.owningNode() and self.structConstraint != port.structConstraint :
                        if port.structureType != newStruct:
                            free = False
                    else:
                        free = port.canChangeStructure(newStruct,checked,selfChek)
            return free

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

    def updatestructConstraint(self,constraint):
        self.structConstraint = constraint
        if constraint in self.owningNode().structConstraints:
            self.owningNode().structConstraints[constraint].append(self)
        else:
            self.owningNode().structConstraints[constraint] = [self]

    @staticmethod
    def jsonEncoderClass():
        return json.JSONEncoder

    @staticmethod
    def jsonDecoderClass():
        return json.JSONDecoder

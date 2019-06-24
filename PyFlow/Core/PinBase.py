from blinker import Signal
import uuid
from copy import deepcopy
import weakref
import json
from nine import str

from PyFlow.Core.Interfaces import IPin
from PyFlow.Core.Common import *
from PyFlow.Core.EvaluationEngine import EvaluationEngine
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
        self.dataBeenSet = Signal(object)
        self.dictChanged = Signal(str)

        self.errorOccured = Signal(object)
        self.errorCleared = Signal()
        self._lastError = None

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
        self._group = ""
        ## Defines is this input pin or output
        self.direction = direction

        # gui class weak ref
        self._wrapper = None
        self.inputWidgetVariant = "DefaultWidget"

        # Constraint ports
        self.constraint = None
        self.structConstraint = None

        # Flags
        self._flags = PinOptions.Storable
        self._origFlags = self._flags
        self._structure = PinStructure.Single
        self._currStructure = self._structure
        self._isAny = False
        self._isArray = False
        self._isDict = False
        self._alwaysList = False
        self._alwaysDict = False
        self._alwaysSingle = False
        self._defaultSupportedDataTypes = self._supportedDataTypes = self.supportedDataTypes()
        self.canChange = False
        self._isDictElement = False
        self.hidden = False

        # DataTypes
        self.super = self.__class__
        self.activeDataType = self.__class__.__name__
        self._keyType = None

        # registration
        self.owningNode().pins.add(self)
        self.owningNode().pinsCreationOrder[self.uid] = self

        # This is for to be able to connect pins by location on node
        self.pinIndex = 0
        if direction == PinDirection.Input:
            self.pinIndex = len(self.owningNode().orderedInputs)
            self.owningNode().orderedInputs[self.pinIndex] = self
        if direction == PinDirection.Output:
            self.pinIndex = len(self.owningNode().orderedOutputs)
            self.owningNode().orderedOutputs[self.pinIndex] = self

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = str(value)

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
        result = list()
        if self.direction == PinDirection.Output:
            for i in getConnectedPins(self):
                connection = {"lhsNodeName": "", "outPinId": 0, "rhsNodeName": "", "inPinId": 0}
                connection["lhsNodeName"] = self.owningNode().getName()
                connection["outPinId"] = self.pinIndex
                connection["rhsNodeName"] = i.owningNode().getName()
                connection["inPinId"] = i.pinIndex
                result.append(connection)

        if self.direction == PinDirection.Input:
            for i in getConnectedPins(self):
                connection = {"lhsNodeName": "", "outPinId": 0, "rhsNodeName": "", "inPinId": 0}
                connection["lhsNodeName"] = i.owningNode().getName()
                connection["outPinId"] = i.pinIndex
                connection["rhsNodeName"] = self.owningNode().getName()
                connection["inPinId"] = self.pinIndex
                result.append(connection)
        return result

    def __repr__(self):
        return "[{0}:{1}:{2}:{3}]".format(self.dataType, self.getName(), self.dirty, self.currentData())

    def isExec(self):
        return False

    def initAsArray(self, bIsArray):
        """Sets this pins to be a list always"""
        self._alwaysList = bool(bIsArray)
        if bool(bIsArray):
            self._alwaysDict = False
        self.setAsArray(bool(bIsArray))

    def initAsDict(self, bIsDict):
        """Sets this pins to be a dict always"""
        self._alwaysDict = bool(bIsDict)
        if bool(bIsDict):
            self._alwaysList = False
        self.setAsDict(bool(bIsDict))

    def setAsArray(self, bIsArray):
        bIsArray = bool(bIsArray)
        if self._isArray == bIsArray:
            return

        self._isArray = bIsArray
        if bIsArray:
            # list pins supports only lists by default
            self.enableOptions(PinOptions.SupportsOnlyArrays)
            self._currStructure = PinStructure.Array
            self._isDict = False
        else:
            self._currStructure = self._structure
        self._data = self.defaultValue()
        self.containerTypeChanged.send()

    def setAsDict(self, bIsDict):
        bIsDict = bool(bIsDict)
        if self._isDict == bIsDict:
            return

        self._isDict = bIsDict
        if bIsDict:
            # list pins supports only lists by default
            self.enableOptions(PinOptions.SupportsOnlyArrays)
            self._currStructure = PinStructure.Dict
            self._isArray = False
        else:
            self._currStructure = self._structure
            self._keyType = None
        self._data = self.defaultValue()
        self.containerTypeChanged.send()

    def isArray(self):
        return self._isArray

    def isDict(self):
        return self._isDict

    @staticmethod
    def IsValuePin():
        return True

    def setWrapper(self, wrapper):
        if self._wrapper is None:
            self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        return self._wrapper

    def deserialize(self, jsonData):
        self.setName(jsonData["name"])
        self.uid = uuid.UUID(jsonData['uuid'])

        for opt in PinOptions:
            if opt.value in jsonData["options"]:
                self.enableOptions(opt)
            else:
                self.disableOptions(opt)

        self.changeStructure(jsonData["structure"])
        self._alwaysList = jsonData['alwaysList']
        self._alwaysSingle = jsonData['alwaysSingle']
        self._alwaysDict = jsonData['alwaysDict']

        try:
            self.setData(json.loads(jsonData['value'], cls=self.jsonDecoderClass()))
        except:
            self.setData(self.defaultValue())

        if jsonData['bDirty']:
            self.setDirty()
        else:
            self.setClean()

    # ISerializable interface
    def serialize(self):

        storable = self.optionEnabled(PinOptions.Storable)

        serializedData = None
        if not self.dataType == "AnyPin":
            if storable:
                serializedData = json.dumps(self.currentData(), cls=self.jsonEncoderClass())
            else:
                serializedData = json.dumps(self.defaultValue(), cls=self.jsonEncoderClass())

        data = {
            'name': self.name,
            'package': self.packageName,
            'fullName': self.getName(),
            'dataType': self.__class__.__name__,
            'direction': int(self.direction),
            'value': serializedData,
            'uuid': str(self.uid),
            'bDirty': self.dirty,
            'linkedTo': list(self.linkedTo),
            'options': [i.value for i in PinOptions if self.optionEnabled(i)],
            'structure': int(self._currStructure),
            'alwaysList': self._alwaysList,
            'alwaysSingle': self._alwaysSingle,
            'alwaysDict': self._alwaysDict
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
        return self.owningNode().name + '_' + self.name

    # IPin interface

    ## This used by node box to suggest nodes by type
    @staticmethod
    def pinDataTypeHint():
        return None

    @staticmethod
    def supportedDataTypes():
        return ()

    def allowedDataTypes(self, checked=[], dataTypes=[], selfChek=True, defaults=False):
        return list(self.supportedDataTypes())

    def checkFree(self, checked=[], selfChek=True):
        return False

    def defaultValue(self):
        if self.isArray():
            return []
        elif self.isDict():
            return pyf_dict("StringPin","AnyPin")
        else:
            return self._defaultValue

    ## retrieving the data
    def getData(self):
        return EvaluationEngine().getPinData(self)

    def clearError(self):
        self._lastError = None
        self.errorCleared.send()

    def setError(self, err):
        self._lastError = str(err)
        self.errorOccured.send(self._lastError)

    ## Setting the data
    def setData(self, data):
        if self.super is None:
            return

        try:
            self.setClean()
            if isinstance(data, dictElement) and not self.optionEnabled(PinOptions.DictElementSuported):
                data = data[1]
            if not self.isArray() and not self.isDict():
                self._data = self.super.processData(data)
            elif self.isArray():
                if isinstance(data, list):
                    self._data = [self.super.processData(i) for i in data]
                else:
                    self._data = [self.super.processData(data)]
            elif self.isDict():
                if isinstance(data, pyf_dict):
                    self._data = pyf_dict(data.keyType, data.valueType)
                    for key, value in data.items():
                        self._data[key] = self.super.processData(value)
                elif isinstance(data, dictElement):
                    self._data.clear()
                    self._data[data[0]] = self.super.processData(data[1])
                else:
                    raise Exception("Non Valid Dict Input")

            if self.direction == PinDirection.Output:
                for i in self.affects:
                    i.setData(self.currentData())
                    i.setClean()
            if self.direction == PinDirection.Input or self.optionEnabled(PinOptions.AlwaysPushDirty):
                push(self)
            self.clearError()
            self.dataBeenSet.send(self)
        except Exception as exc:
            self.setError(exc)
            self.setDirty()
        if self._lastError is not None:
            self.owningNode().setError(self._lastError)
            wrapper = self.owningNode().getWrapper()
            if wrapper:
                wrapper.update()

    ## Calling execution pin
    def call(self, *args, **kwargs):
        if self.owningNode().isValid():
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

    @property
    def currentStructure(self):
        return self._currStructure

    @structureType.setter
    def structureType(self, structure):
        self._structure = structure
        self._currStructure = structure

    # PinBase methods

    def kill(self, *args, **kwargs):
        self.disconnectAll()
        if self in self.owningNode().pins:
            self.owningNode().pins.remove(self)
        if self.uid in self.owningNode().pinsCreationOrder:
            self.owningNode().pinsCreationOrder.pop(self.uid)
        if self.pinIndex in self.owningNode().orderedInputs:
            self.owningNode().orderedInputs.pop(self.pinIndex)
        if self.pinIndex in self.owningNode().orderedOutputs:
            self.owningNode().orderedOutputs.pop(self.pinIndex)
        self.killed.send(self)
        clearSignal(self.killed)

    def currentData(self):
        if self._data is None:
            return self._defaultValue
        return self._data

    def aboutToConnect(self, other):
        self.changeStructure(other._currStructure)
        self.onPinConnected.send(other)

    def changeStructure(self, newStruct, init=False):
        free = self.canChangeStructure(newStruct, [], init=init)
        if free:
            self.updateConstrainedPins(set(), newStruct, init, connecting=True)
            self.structureType = newStruct

    def canChangeStructure(self, newStruct, checked=[], selfChek=True, init=False):
        if not init and (self._alwaysList or self._alwaysSingle or self._alwaysDict):
            return False
        if self.structConstraint is None and self.structureType == PinStructure.Multi:
            return True
        elif self.structureType != PinStructure.Multi:
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
            if selfChek:
                def testfree():
                    free = False
                    for pin in getConnectedPins(self):
                        if pin._structure == PinStructure.Multi:
                            free = True
                        else:
                            free = False
                            break  
                    return free                  
                if self._currStructure == PinStructure.Single and newStruct == PinStructure.Array and not self.optionEnabled(PinOptions.ArraySupported) and self.hasConnections():
                    free = testfree()
                elif self._currStructure == PinStructure.Single and newStruct == PinStructure.Dict and not self.optionEnabled(PinOptions.DictSupported) and self.hasConnections():
                    free = testfree()                      
                elif self._currStructure == PinStructure.Array and newStruct == PinStructure.Single and self.optionEnabled(PinOptions.SupportsOnlyArrays) and self.hasConnections():
                    free = testfree()
                elif self._currStructure == PinStructure.Array and newStruct == PinStructure.Dict and self.hasConnections():
                    free = testfree()                    
                elif self._currStructure == PinStructure.Dict and newStruct == PinStructure.Array and self.hasConnections():
                    free = testfree()    
                elif self._currStructure == PinStructure.Dict and newStruct == PinStructure.Single and self.optionEnabled(PinOptions.SupportsOnlyArrays) and self.hasConnections():
                    free = testfree()
            if free:
                for port in self.owningNode().structConstraints[self.structConstraint] + con:
                    if port not in checked:
                        checked.append(port)
                        free = port.canChangeStructure(newStruct, checked, True, init=init)
                        if not free:
                            break
            return free

    def updateConstrainedPins(self, traversed, newStruct, init=False, connecting=False):
        nodePins = set()
        if self.structConstraint is not None:
            nodePins = set(self.owningNode().structConstraints[self.structConstraint])
        else:
            nodePins = set([self])
        for connectedPin in getConnectedPins(self):
            if connectedPin.structureType == PinStructure.Multi:
                if connectedPin.canChangeStructure(self._currStructure, init=init):
                    nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                neighbor.setAsArray(newStruct == PinStructure.Array)
                neighbor.setAsDict(newStruct == PinStructure.Dict)
                if connecting:
                    if init:
                        neighbor._alwaysList = newStruct == PinStructure.Array
                        neighbor._alwaysSingle = newStruct == PinStructure.Single
                        neighbor._alwaysDict = newStruct == PinStructure.Dict
                    neighbor._currStructure = newStruct
                    neighbor.disableOptions(PinOptions.ArraySupported)
                    neighbor.disableOptions(PinOptions.DictSupported)
                    if newStruct == PinStructure.Array:
                        neighbor.enableOptions(PinOptions.ArraySupported)
                    elif newStruct == PinStructure.Dict:
                        neighbor.enableOptions(PinOptions.DictSupported)   
                    elif newStruct == PinStructure.Multi:
                        neighbor.enableOptions(PinOptions.ArraySupported)
                        neighbor.enableOptions(PinOptions.DictSupported)
                    elif newStruct == PinStructure.Single:
                        neighbor.disableOptions(PinOptions.SupportsOnlyArrays)
                else:
                    neighbor._currStructure = neighbor._structure
                    neighbor._data = neighbor.defaultValue()
                traversed.add(neighbor)
                neighbor.setData(neighbor.defaultValue())
                neighbor.updateConstrainedPins(traversed, newStruct, init, connecting=connecting)

    def pinConnected(self, other):
        push(self)
        if self.isDict():
            self.updateConectedDicts([],self._data.keyType)   

    def pinDisconnected(self, other):
        self.onPinDisconnected.send(other)
        push(other)

    def canChangeTypeOnConection(self, checked=[], can=True, extraPins=[], selfChek=True):
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            return False
        con = []
        neis = []
        if selfChek:
            if self.hasConnections():
                for c in getConnectedPins(self):
                    if c not in checked:
                        con.append(c)
        else:
            checked.append(self)
        if self.constraint:
            neis = self.owningNode().constraints[self.constraint]
        for port in neis + con + extraPins:
            if port not in checked and can:
                checked.append(port)
                can = port.canChangeTypeOnConection(checked, can, selfChek=True)
        return can

    def getDictElementNode(self,checked=[],node=None):
        if self.owningNode().__class__.__name__ == "makeDictElement":
            return self.owningNode()
        con = []
        neis = []
        if self.hasConnections() and self.direction == PinDirection.Input:
            for c in getConnectedPins(self):
                if c not in checked:
                    con.append(c)
        if self.constraint:
            neis = self.owningNode().constraints[self.constraint]                    
        for port in con + neis:
            if port not in checked and node == None:
                checked.append(port)
                node = port.getDictElementNode(checked,node)
        return node

    def getDictNode(self,checked=[],node=None):
        if self.owningNode().__class__.__name__ == "makeDict" :#and self.name == "data":
            return self.owningNode()
        con = []
        neis = []
        if self.hasConnections():
            for c in getConnectedPins(self):
                if c not in checked:
                    con.append(c)
        if self.constraint:
            neis = self.owningNode().constraints[self.constraint]                    
        for port in con + neis:
            if port not in checked and node == None:
                checked.append(port)
                node = port.getDictNode(checked,node)
        return node

    def supportDictElement(self,checked=[],can=True,selfChek=True):
        if not self.optionEnabled(PinOptions.DictElementSuported):
            return False
        con = []
        neis = []
        if selfChek:
            if self.hasConnections() and self.direction == PinDirection.Input:
                for c in getConnectedPins(self):
                    if c not in checked:
                        con.append(c)
        else:
            checked.append(self)
        if self.constraint and self.owningNode().__class__.__name__ != "makeDictElement":
            neis = self.owningNode().constraints[self.constraint]
        for port in neis + con:
            if port not in checked and can:
                checked.append(port)
                can = port.supportDictElement(checked, can, selfChek=True)
        return can

    def supportOnlyDictElement(self, checked=[], can=False, selfChek=True):
        if self.isDict():
            return True
        con = []
        neis = []
        if selfChek:
            if self.hasConnections() and self.direction == PinDirection.Output:
                for c in getConnectedPins(self):
                    if c not in checked:
                        con.append(c)
        else:
            checked.append(self)
        if self.constraint and self.owningNode().__class__.__name__ != "makeDictElement":
            neis = self.owningNode().constraints[self.constraint]
        for port in neis + con:
            if port not in checked and not can:
                checked.append(port)
                can = port.supportOnlyDictElement(checked, can, selfChek=True)
        return can

    def updateConectedDicts(self, checked=[], keyType=None):
        if not self.isDict():
            return
        con = []
        neis = []
        if self.hasConnections():
            for c in getConnectedPins(self):
                if c not in checked:
                    con.append(c)
        if self.constraint:
            neis = self.owningNode().constraints[self.constraint]
        for port in con + neis:
            if port not in checked and port.isDict():
                checked.append(port)
                port._keyType = keyType
                if port._data.keyType != keyType:
                    port._data = pyf_dict(keyType, port.dataType)
                port.dictChanged.send(keyType)
                if port.getWrapper():
                    port.getWrapper()().update()
                port.updateConectedDicts(checked, keyType)

    def setClean(self):
        self.dirty = False
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i.dirty = False

    def setDirty(self):
        if self.isExec():
            return
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def hasConnections(self):
        numConnections = 0
        if self.direction == PinDirection.Input:
            numConnections += len(self.affected_by)
        elif self.direction == PinDirection.Output:
            numConnections += len(self.affects)
        return numConnections > 0

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

    def updatestructConstraint(self, constraint):
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

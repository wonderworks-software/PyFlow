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
    """
    **Base class for pins**

    This is the base class that stores the data in the graph.
    This class is intended to be subclassed for each new registered data type you want to create.

    :param _packageName: This holds the package where the sub classed pin is registered.
                         It is not intended to be set by developer, PyFlow automatically fills this property at
                         registration point
    :type _packageName: str

    Signals:
        * **serializationHook** : Fired when Serialize Pin called, so Ui wrapers can append data to the serialization
        * **onPinConnected** : Fired when a new connection is made to this Pin, sends other Pin
        * **onPinDisconnected** : Fired when some disconnection is made to this Pin, sends other Pin
        * **nameChanged** : Fired when pin.setName() called, sends New Name
        * **killed** : Fired when Pin gets deleted
        * **onExecute** : Fired when Pin execution gets called
        * **containerTypeChanged** : Fired when Pin Structure Changes
        * **dataBeenSet** : Fired when data changes, sends New Data
        * **dictChanged** : Fired when current structure changes to :py:const:`PyFlow.Core.Common.PinStructure.Dict`, sends Dict key DataType
        * **errorOccurred** : Fired when some error fired, like incorrect dataType set, sends ocurred Error
        * **errorCleared** : Fired when error cleared

    :ivar owningNode: Weak reference to owning node
    :ivar reconnectionPolicy: What to do if connect with busy pin. Used when :attr:`~PyFlow.Core.Common.PinOptions.AllowMultipleConnections` flag is disabled
    :ivar dirty: This flag for lazy evaluation
    :ivar affects: List of pins this pin affects to
    :ivar affected_by: List of pins that affects to this pin
    :ivar name: Pin name
    :ivar direction: Pin direction
    :ivar inputWidgetVariant: Input widget variant tag
    :ivar constraint: **description here**
    :ivar structConstraint: **description here**
    :ivar super: **description here**
    :ivar activeDataType: Current data type of this pin. Used by AnyPin
    :ivar pinIndex: Position of this pin on node
    """
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
        self.reconnectionPolicy = PinReconnectionPolicy.DisconnectIfHasConnections
        self.dirty = True
        self.affects = set()
        self.affected_by = set()

        self.name = name
        self._group = ""
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
        if direction == PinDirection.Output:
            self.pinIndex = len(self.owningNode().orderedOutputs)

    @property
    def group(self):
        """Pin group

        This is just a tag which can be used in ui level

        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, value):
        self._group = str(value)

    def enableOptions(self, *options):
        """Enables flags on pin instance

        Example:

        >>> self.pinInstance.enableOptions(PinOptions.RenamingEnabled)

        You can also pass array/set of flags

        >>> self.pinInstance.enableOptions({PinOptions.RenamingEnabled, PinOptions.Dynamic})

        This is equivalent of

        >>> self.pinInstance.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        """
        for option in options:
            self._flags = self._flags | option
        self._origFlags = self._flags

    def disableOptions(self, *options):
        """Same as :meth:`~PyFlow.Core.PinBase.PinBase.enableOptions` but inverse
        """
        for option in options:
            self._flags = self._flags & ~option
        self._origFlags = self._flags

    def optionEnabled(self, option):
        """Is option enabled or not

        :param option: Option to check
        :type option: :class:`~PyFlow.Core.Common.PinOptions`
        :rtype: bool
        """
        return bool(self._flags & option)

    def isAny(self):
        """Wheter this pin of type Any or not

        :rtype: bool
        """
        return self._isAny

    @property
    def packageName(self):
        """Returns name of package this pin belongs to

        :rtype: bool
        """
        return self._packageName

    @property
    def linkedTo(self):
        """store connection from pins

        from left hand side to right hand side

        .. code-block:: python

            {
                "lhsNodeName": "", "outPinId": 0,
                "rhsNodeName": "", "inPinId": 0
            }

        where pin id is order in which pin was added to node

        :returns: Serialized connections
        :rtype: list(dict)
        """
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
        return "[{0}:{1}:{2}:{3}]".format(self.dataType, self.getFullName(), self.dirty, self.currentData())

    def isExec(self):
        """Returns whether this is exec pin or not

        :rtype: bool
        """
        return False

    def initAsArray(self, bIsArray):
        """Sets this pins to be a list always

        :param bIsArray: Define as array
        :type bIsArray: bool
        """
        self._alwaysList = bool(bIsArray)
        if bool(bIsArray):
            self._alwaysDict = False
        self.setAsArray(bool(bIsArray))

    def initAsDict(self, bIsDict):
        """Sets this pins to be a dict always

        :param bIsArray: Define as dict
        :type bIsArray: bool
        """
        self._alwaysDict = bool(bIsDict)
        if bool(bIsDict):
            self._alwaysList = False
        self.setAsDict(bool(bIsDict))

    def setAsArray(self, bIsArray):
        """Sets this pins to be a list

        :param bIsArray: Define as Array
        :type bIsArray: bool
        """
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
        """Sets this pins to be a dict

        :param bIsArray: Define as Array
        :type bIsArray: bool
        """
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
        """Returns whether this pin is array or not

        :rtype: bool
        """
        return self._isArray

    def isDict(self):
        """Returns whether this pin is dict or not

        :rtype: bool
        """
        return self._isDict

    def setWrapper(self, wrapper):
        """Sets ui wrapper instance

        :param wrapper: Whatever ui class that represents this pin
        """
        if self._wrapper is None:
            self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        """Returns ui wrapper instance
        """
        return self._wrapper

    def deserialize(self, jsonData):
        """Restores itself from supplied serialized data

        :param jsonData: Json representation of pin
        :type jsonData: dict
        """
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

    def serialize(self):
        """Serializes itself to json

        :rtype: dict
        """
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
            'fullName': self.getFullName(),
            'dataType': self.__class__.__name__,
            'direction': int(self.direction),
            'value': serializedData,
            'uuid': str(self.uid),
            'bDirty': self.dirty,
            'linkedTo': list(self.linkedTo),
            'pinIndex': self.pinIndex,
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

    @property
    def uid(self):
        """Returns unique identifier

        :rtype: :class:`uuid.UUID`
        """
        return self._uid

    @uid.setter
    def uid(self, value):
        if not value == self._uid:
            self._uid = value

    def setName(self, name, force=False):
        """Sets pin name and fires events

        :param name: New pin name
        :type name: str
        :param force: If True - name will be changed even if option :attr:`~PyFlow.Core.Common.PinOptions.RenamingEnabled` is turned off
        :type force: bool
        :returns: Whether renaming performed or not
        :rtype: bool
        """
        if not force:
            if not self.optionEnabled(PinOptions.RenamingEnabled):
                return False
        if name == self.name:
            return False
        self.name = self.owningNode().getUniqPinName(name)
        self.nameChanged.send(self.name)
        return True

    def getFullName(self):
        """Returns full pin name, including node name

        :rtype: str
        """
        return self.owningNode().name + '_' + self.name

    def allowedDataTypes(self, checked=[], dataTypes=[], selfCheck=True, defaults=False):
        return list(self.supportedDataTypes())

    def checkFree(self, checked=[], selfCheck=True):
        return False

    def defaultValue(self):
        """Returns default value of this pin
        """
        if self.isArray():
            return []
        elif self.isDict():
            return PFDict("StringPin", "AnyPin")
        else:
            return self._defaultValue

    def getData(self):
        """Returns pin value

        If something is connected to this pin, graph will be evaluated

        .. seealso:: :class:`~PyFlow.Core.EvaluationEngine.DefaultEvaluationEngine_Impl`
        """
        return EvaluationEngine().getPinData(self)

    def clearError(self):
        """Clears any last error on this pin and fires event
        """
        if self._lastError is not None:
            self._lastError = None
            self.errorCleared.send()

    def setError(self, err):
        """Marks this pin as invalid by setting error message to it. Also fires event

        :param err: Error message
        :type err: str
        """
        self._lastError = str(err)
        self.errorOccured.send(self._lastError)

    def validateArray(self, array, func):
        valid = True
        if isinstance(array, list):
            for i in array:
                self.validateArray(i, func)
        else:
            func(array)
        return valid

    def setData(self, data):
        """Sets value to pin

        :param data: Data to be set
        :type data: object
        """
        if self.super is None:
            return
        try:
            self.setClean()
            if isinstance(data, DictElement) and not self.optionEnabled(PinOptions.DictElementSupported):
                data = data[1]
            if not self.isArray() and not self.isDict():
                self._data = self.super.processData(data)
            elif self.isArray():
                if isinstance(data, list):
                    if self.validateArray(data, self.super.processData):
                        self._data = data
                    else:
                        raise Exception("Some Array Input is not valid Data")
                else:
                    self._data = [self.super.processData(data)]
            elif self.isDict():
                if isinstance(data, PFDict):
                    self._data = PFDict(data.keyType, data.valueType)
                    for key, value in data.items():
                        self._data[key] = self.super.processData(value)
                elif isinstance(data, DictElement) and len(data)==2:
                    self._data.clear()
                    self._data[data[0]] = self.super.processData(data[1])

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

    def call(self, *args, **kwargs):
        if self.owningNode().isValid():
            self.onExecute.send(*args, **kwargs)

    def disconnectAll(self):
        if self.direction == PinDirection.Input:
            for o in list(self.affected_by):
                disconnectPins(self, o)
            self.affected_by.clear()

        if self.direction == PinDirection.Output:
            for i in list(self.affects):
                disconnectPins(self, i)
            self.affects.clear()

    @property
    def dataType(self):
        """Returns data type of this pin

        :rtype: str
        """
        return self.__class__.__name__

    @property
    def structureType(self):
        """Returns current structure of this pin

        :rtype: :class:`~PyFlow.Core.Common.PinStructure`
        """
        return self._structure

    @structureType.setter
    def structureType(self, structure):
        self._structure = structure
        self._currStructure = structure

    # PinBase methods

    def kill(self, *args, **kwargs):
        """Deletes this pin
        """
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
        """Returns current value of this pin, without any graph evaluation

        :rtype: object
        """
        if self._data is None:
            return self._defaultValue
        return self._data

    def aboutToConnect(self, other):
        """This method called right before two pins connected

        :param other: Pin which this pin is going to be connected with
        :type other: :class:`~PyFlow.Core.PinBase.PinBase`
        """
        self.changeStructure(other._currStructure)
        self.onPinConnected.send(other)

    def getCurrentStructure(self):
        """Returns this pin structure type

        :rtype: :class:`~PyFlow.Core.Common.PinStructure`
        """
        if self.structureType == PinStructure.Multi:
            if self._alwaysSingle:
                return PinStructure.Single
            elif self._alwaysList:
                return PinStructure.Array
            elif self._alwaysDict:
                return PinStructure.Dict
            else:
                return self.structureType
        else:
            return self.structureType

    def changeStructure(self, newStruct, init=False):
        """Changes this pin structure type

        :param newStruct: Target structure
        :type newStruct: :class:`~PyFlow.Core.Common.PinStructure`
        :param init: **docs goes here**
        :type init: bool
        """
        free = self.canChangeStructure(newStruct, [], init=init)
        if free:
            self.updateConstrainedPins(set(), newStruct, init, connecting=True)

    def canChangeStructure(self, newStruct, checked=[], selfCheck=True, init=False):
        """Recursive function to determine if pin can change its structure

        :param newStruct: New structure we want to apply
        :type newStruct: string
        :param checked: Already visited pins, defaults to []
        :type checked: list, optional
        :param selfCheck: Define if check pin itself for connected pins, defaults to True
        :type selfCheck: bool, optional
        :param init: Initialization flag, if set multi pins can became other structure and don't be able to change after new call with init=True, defaults to False
        :type init: bool, optional
        :returns: True if pin can change structure to newStruct
        :rtype: bool
        """
        if not init and (self._alwaysList or self._alwaysSingle or self._alwaysDict):
            return False
        if self.structConstraint is None and self.structureType == PinStructure.Multi:
            return True
        elif self.structureType != PinStructure.Multi:
            return False
        else:
            con = []
            if selfCheck:
                free = not self.hasConnections()
                if not free:
                    for c in getConnectedPins(self):
                        if c not in checked:
                            con.append(c)
            else:
                free = True
                checked.append(self)
            free = True
            if selfCheck:
                def testfree():
                    free = False
                    for pin in getConnectedPins(self):
                        if pin._structure == PinStructure.Multi:
                            free = True
                        else:
                            free = False
                            break
                    return free
                if any([self._currStructure == PinStructure.Single and newStruct == PinStructure.Array  and not self.optionEnabled(PinOptions.ArraySupported) and self.hasConnections(),
                        self._currStructure == PinStructure.Single and newStruct == PinStructure.Dict   and not self.optionEnabled(PinOptions.DictSupported)  and self.hasConnections(),
                        self._currStructure == PinStructure.Array  and newStruct == PinStructure.Single and self.optionEnabled(PinOptions.SupportsOnlyArrays) and self.hasConnections(),
                        self._currStructure == PinStructure.Dict   and newStruct == PinStructure.Single and self.optionEnabled(PinOptions.SupportsOnlyArrays) and self.hasConnections(),
                        self._currStructure == PinStructure.Array  and newStruct == PinStructure.Dict   and self.hasConnections(),
                        self._currStructure == PinStructure.Dict   and newStruct == PinStructure.Array  and self.hasConnections()]):
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
            self.updateConnectedDicts([], self._data.keyType)

    def pinDisconnected(self, other):
        self.onPinDisconnected.send(other)
        push(other)

    def canChangeTypeOnConnection(self, checked=[], can=True, extraPins=[], selfCheck=True):
        """Recursive function to determine if pin can change its dataType

        :param checked: Already visited pins, defaults to []
        :type checked: list, optional
        :param can: Variable Updated during iteration, defaults to True
        :type can: bool, optional
        :param extraPins: extra pins, non constrained or connected to this pin but that want to check also, defaults to []
        :type extraPins: list, optional
        :param selfCheck: Define if check pin itself for connected pins, defaults to True
        :type selfCheck: bool, optional
        :returns: True if pin can becabe other dataType
        :rtype: bool
        """
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            return False
        con = []
        neis = []
        if selfCheck:
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
                can = port.canChangeTypeOnConnection(checked, can, selfCheck=True)
        return can

    def getDictElementNode(self, checked=[], node=None):
        """Get the connected :py:class:`PyFlow.Packages.PyFlowBase.Nodes.makeDictElement.makeDictElement` to this pin recursively

        :param checked: Currently visited pins, defaults to []
        :type checked: list, optional
        :param node: founded node, defaults to None
        :rtype: :class:`~PyFlow.Core.NodeBase.NodeBase` or None
        """
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
                node = port.getDictElementNode(checked, node)
        return node

    def getDictNode(self, checked=[], node=None):
        """Get the connected :py:class:`PyFlow.Packages.PyFlowBase.Nodes.makeDict.makeDict` or
        :py:class:`PyFlow.Packages.PyFlowBase.Nodes.makeAnyDict.makeAnyDict` to this pin recursively

        :param checked: Currently visited pins, defaults to []
        :type checked: list, optional
        :param node: founded node, defaults to None
        :returns: founded node or None if not found
        """
        if self.owningNode().__class__.__name__ in ["makeDict", "makeAnyDict"]:
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
                node = port.getDictNode(checked, node)
        return node

    def supportDictElement(self, checked=[], can=True, selfCheck=True):
        """Iterative functions that search in all connected pins to see if they support DictElement nodes.

        :param checked: Already visited pins, defaults to []
        :type checked: list, optional
        :param can: this is the variable that will be actualized during the recursive function, defaults to False
        :type can: bool, optional
        :param selfCheck: Define if look itself or no, defaults to True
        :type selfCheck: bool, optional
        :returns: True if can connect DictElement nodes to this pin
        :rtype: bool
        """
        if not self.optionEnabled(PinOptions.DictElementSupported):
            return False
        con = []
        neis = []
        if selfCheck:
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
                can = port.supportDictElement(checked, can, selfCheck=True)
        return can

    def supportOnlyDictElement(self, checked=[], can=False, selfCheck=True):
        """Iterative Functions that search in all connected pins to see if they support only DictElement nodes, this
        is done for nodes like makeDict and simmilars.

        :param checked: Already Visited Pins, defaults to []
        :type checked: list, optional
        :param can: this is the variable that will be actualized during the recursive function, defaults to False
        :type can: bool, optional
        :param selfCheck: Defines if look itself or no, defaults to True
        :type selfCheck: bool, optional
        :returns: True if can connect only DictElement and Dicts nodes to this Pin
        :rtype: bool
        """
        if self.isDict():
            return True
        con = []
        neis = []
        if selfCheck:
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
                can = port.supportOnlyDictElement(checked, can, selfCheck=True)
        return can

    def updateConnectedDicts(self, checked=[], keyType=None):
        """Iterate over connected dicts pins and DictElements pins updating key data type

        :param checked: Already visited pins, defaults to []
        :type checked: list, optional
        :param keyType: KeyDataType to set, defaults to None
        :type keyType: string, optional
        """
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
                    port._data = PFDict(keyType, port.dataType)
                port.dictChanged.send(keyType)
                if port.getWrapper():
                    port.getWrapper()().update()
                port.updateConnectedDicts(checked, keyType)

    def setClean(self):
        """Sets dirty flag to True
        """
        self.dirty = False
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i.dirty = False

    def setDirty(self):
        """Sets dirty flag to True
        """
        if self.isExec():
            return
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def hasConnections(self):
        """Return the number of connections this pin has

        :rtype: int
        """
        numConnections = 0
        if self.direction == PinDirection.Input:
            numConnections += len(self.affected_by)
        elif self.direction == PinDirection.Output:
            numConnections += len(self.affects)
        return numConnections > 0

    def setDefaultValue(self, val):
        """In python, all user-defined classes are mutable
        So make sure to store separate copy of value
        For example if this is a Matrix, default value will be changed each time data has been set in original Matrix

        :param val: defaultValue
        :type val: object
        """
        self._defaultValue = deepcopy(val)

    def updateConstraint(self, constraint):
        self.constraint = constraint
        if constraint in self.owningNode().constraints:
            self.owningNode().constraints[constraint].append(self)
        else:
            self.owningNode().constraints[constraint] = [self]

    def updateStructConstraint(self, constraint):
        self.structConstraint = constraint
        if constraint in self.owningNode().structConstraints:
            self.owningNode().structConstraints[constraint].append(self)
        else:
            self.owningNode().structConstraints[constraint] = [self]

    @staticmethod
    def IsValuePin():
        """Returns whether this pin is value pin or not

        :rtype: bool
        """
        return True

    @staticmethod
    def pinDataTypeHint():
        """Hint of what data type is this pin, as well as default value for this data type.

        Used to easily find pin classes by type id.

        :rtype: tuple(str, object)
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('pinDataTypeHint method of PinBase is not implemented')

    @staticmethod
    def supportedDataTypes():
        return ()

    @staticmethod
    def jsonEncoderClass():
        """Returns json encoder class for this pin
        """
        return json.JSONEncoder

    @staticmethod
    def jsonDecoderClass():
        """Returns json decoder class for this pin
        """
        return json.JSONDecoder

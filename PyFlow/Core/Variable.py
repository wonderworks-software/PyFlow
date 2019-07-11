from nine import str
from blinker import Signal
import json

from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import IItemBase


class Variable(IItemBase):
    """Variable representation
    """
    def __init__(self, graph, value, name, dataType, accessLevel=AccessLevel.public, structure=PinStructure.Single, uid=None):
        super(Variable, self).__init__()
        # signals
        self.nameChanged = Signal(str)
        self.valueChanged = Signal(str)
        self.dataTypeChanged = Signal(str)
        self.structureChanged = Signal(str)
        self.accessLevelChanged = Signal(str)
        self.packageNameChanged = Signal(str)
        self.uuidChanged = Signal(object)
        self.killed = Signal()

        self.graph = graph

        self._name = name
        self._value = value
        self._dataType = dataType
        self._structure = structure
        self._accessLevel = accessLevel
        self._packageName = None
        self._uid = uuid.uuid4() if uid is None else uid
        assert(isinstance(self._uid, uuid.UUID))
        self.updatePackageName()
        self._uiWrapper = None

    def getWrapper(self):
        if self._uiWrapper is not None:
            return self._uiWrapper()
        return None

    def setWrapper(self, wrapper):
        if self._uiWrapper is None:
            self._uiWrapper = weakref.ref(wrapper)

    def location(self):
        return self.graph.location()

    def findRefs(self):
        """returns all getVar and setVar instances for this node
        """
        return self.graph.graphManager.findVariableRefs(self)

    def updatePackageName(self):
        self._packageName = findPinClassByType(self._dataType)._packageName

    @property
    def packageName(self):
        return self._packageName

    @packageName.setter
    def packageName(self, value):
        assert(isinstance(value, str))
        self._packageName = value
        self.packageNameChanged.send(value)

    @property
    def accessLevel(self):
        return self._accessLevel

    @accessLevel.setter
    def accessLevel(self, value):
        assert(isinstance(value, AccessLevel))
        self._accessLevel = value
        self.accessLevelChanged.send(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert(isinstance(value, str))
        self._name = value
        self.nameChanged.send(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # type checking if this variable is not of any type
        if not self.dataType == 'AnyPin':
            supportedDataTypes = findPinClassByType(self.dataType).supportedDataTypes()
            if self.dataType not in supportedDataTypes:
                return

        try:
            if self._value != value:
                self._value = value
                self.valueChanged.send(value)
        except:
            self._value = value
            self.valueChanged.send(value)

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        assert(isinstance(value, str))
        if value != self._dataType:
            self._dataType = value
            self.updatePackageName()
            self.value = getPinDefaultValueByType(self._dataType)
            self.dataTypeChanged.send(value)

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        assert(isinstance(value, PinStructure))
        if value != self._structure:
            self._structure = value
            if self._structure == PinStructure.Array:
                self.value = list()
            self.structureChanged.send(self._structure)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        assert(isinstance(value, uuid.UUID))
        self.graph.getVars()[value] = self.graph.getVars().pop(self._uid)
        self._uid = value

    def serialize(self):
        pinClass = findPinClassByType(self.dataType)

        template = Variable.jsonTemplate()

        uidString = str(self.uid)

        template['name'] = self.name
        if self.dataType == 'AnyPin':
            template['value'] = None
        else:
            template['value'] = json.dumps(self.value, cls=pinClass.jsonEncoderClass())
        template['dataType'] = self.dataType
        template['structure'] = self.structure.name
        template['accessLevel'] = self.accessLevel.name
        template['package'] = self._packageName
        template['uuid'] = uidString

        return template

    @staticmethod
    def deserialize(graph, jsonData, *args, **kwargs):
        name = jsonData['name']
        dataType = jsonData['dataType']

        if dataType != "AnyPin":
            pinClass = findPinClassByType(dataType)
            value = json.loads(jsonData['value'], cls=pinClass.jsonDecoderClass())
        else:
            value = getPinDefaultValueByType("AnyPin")

        accessLevel = AccessLevel[jsonData['accessLevel']]
        structure = PinStructure[jsonData['structure']]
        uid = uuid.UUID(jsonData['uuid'])
        return Variable(graph, value, name, dataType, accessLevel, structure, uid)

    @staticmethod
    def jsonTemplate():
        template = {
            'name': None,
            'value': None,
            'dataType': None,
            'accessLevel': None,
            'package': None,
            'uuid': None
        }
        return template

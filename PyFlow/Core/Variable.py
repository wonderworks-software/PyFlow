from blinker import Signal
import json

from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import ISerializable


class Variable(ISerializable):

    nameChanged = Signal()
    valueChanged = Signal()
    dataTypeChanged = Signal()
    accessLevelChanged = Signal()
    packageNameChanged = Signal()
    uuidChanged = Signal()
    killed = Signal()

    def __init__(self, value, name, dataType, accessLevel=AccessLevel.public, uid=None):
        super(Variable, self).__init__()
        assert(isinstance(name, str))
        assert(isinstance(dataType, str))
        self._name = name
        self._value = value
        self._dataType = dataType
        self._accessLevel = accessLevel
        self._packageName = None
        self._uid = uuid.uuid4() if uid is None else uid
        assert(isinstance(self._uid, uuid.UUID))
        self.updatePackageName()

    def updatePackageName(self):
        self._packageName = findPinClassByType(self._dataType).packageName()

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
            defaultValue = getPinDefaultValueByType(self.dataType)
            assert(isinstance(value, type(defaultValue))), "type error! rhs value type is {0}, but variable type is {1}".format(type(value), type(defaultValue))
        self._value = value
        self.valueChanged.send(value)

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        assert(isinstance(value, str))
        self._dataType = value
        self.updatePackageName()
        self.value = getPinDefaultValueByType(self._dataType)
        self.dataTypeChanged.send(value)

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        assert(isinstance(value, uuid.UUID))
        self._uid = value
        self.uuidChanged.send(value)

    def serialize(self):
        pinClass = findPinClassByType(self.dataType)

        template = Variable.jsonTemplate()

        template['name'] = self.name
        template['value'] = json.dumps(self.value, cls=pinClass.jsonEncoderClass()) if not pinClass.isPrimitiveType() else self.value
        template['dataType'] = self.dataType
        template['accessLevel'] = self.accessLevel.value
        template['package'] = self._packageName
        template['uuid'] = str(self.uid)

        return template

    @staticmethod
    def deserialize(jsonData):
        name = jsonData['name']
        dataType = jsonData['dataType']

        pinClass = findPinClassByType(dataType)
        value = jsonData['value'] if pinClass.isPrimitiveType() else json.loads(jsonData['value'], cls=pinClass.jsonDecoderClass())

        accessLevel = AccessLevel(jsonData['accessLevel'])
        uid = uuid.UUID(json['uuid'])
        return Variable(value, name, dataType, accessLevel, uid)

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

from blinker import Signal
import json
from Qt import QtGui

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow import getAllPinClasses
from PyFlow import CreateRawPin
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType


class AnyPin(PinBase):
    """doc string for AnyPin"""

    def __init__(self, name, parent, direction, **kwargs):
        super(AnyPin, self).__init__(name, parent, direction, **kwargs)
        self.typeChanged = Signal(str)
        self.dataTypeBeenSet = Signal()
        self.setDefaultValue(None)
        self._isAny = True
        self.super = AnyPin
        self.activeDataType = self.__class__.__name__
        # if True, setType and setDefault will work only once
        self.singleInit = False
        self.enableOptions(PinOptions.ChangeTypeOnConnection)
        self._defaultSupportedDataTypes = self._supportedDataTypes = tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])


    @PinBase.dataType.getter
    def dataType(self):
        return self.activeDataType

    @staticmethod
    def supportedDataTypes():
        return tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def defColor():
        return (255, 255, 255, 255)

    @staticmethod
    def color():
        return (255, 255, 255, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'AnyPin', None

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
                
            #if self.activeDataType != self.__class__.__name__:
            #    assert(self.super is not None)
        if self.activeDataType == self.__class__.__name__:
            for pin in [pin for pin in getAllPinClasses() if pin.IsValuePin()]:
                if type(getPinDefaultValueByType(pin.__name__)) == type(data):
                    if pin.__name__ != self.__class__.__name__:
                        self.setType(pin.__name__)
                        print pin.__name__
                        break
                else:
                    self.super = None
        try:
            if not self.isArray():
                data = self.super.processData(data)
            else:
                data = [self.super.processData(i) for i in data]
            self._lastError = None
        except Exception as e:
            data = getPinDefaultValueByType(self.activeDataType)
            self._lastError = e
        self.owningNode().checkForErrors()

        self._data = data
        PinBase.setData(self, self._data)

    def serialize(self):
        dt = super(AnyPin, self).serialize()
        constrainedType = self.activeDataType
        if constrainedType != self.__class__.__name__:
            pinClass = findPinClassByType(constrainedType)
            # serialize with active type's encoder
            dt['value'] = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
            dt['currDataType'] = constrainedType
        return dt

    def deserialize(self, jsonData):
        super(AnyPin, self).deserialize(jsonData)
        if "currDataType" in jsonData:
            self.setType(jsonData["currDataType"])

    def pinConnected(self, other):
        super(AnyPin, self).pinConnected(other)

    def aboutToConnect(self, other):
        if self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            dataType = other.dataType
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, False, other))
        super(AnyPin, self).aboutToConnect(other)

    def pinDisconnected(self, other):
        super(AnyPin, self).pinDisconnected(other)

    def updateOnConnectionCallback(self, pin, dataType, init=False, other=None):
        free = pin.checkFree([])
        if free:
            if (dataType == "AnyPin" and not init):
                if not other:
                    return
                else:
                    if pin.dataType != "AnyPin" and pin.dataType in other.allowedDataTypes([], other._supportedDataTypes) and other.optionEnabled(PinOptions.ChangeTypeOnConnection):
                        dataType = pin.dataType

            if any([dataType in pin.allowedDataTypes([], pin._supportedDataTypes),
                    dataType == "AnyPin",
                    (pin.checkFree([], False) and dataType in pin.allowedDataTypes([], pin._defaultSupportedDataTypes, defaults=True))]):
                a = pin.setType(dataType)
                if a:
                    if other:
                        if pin.optionEnabled(PinOptions.ChangeTypeOnConnection):
                            pin._supportedDataTypes = other.allowedDataTypes([], other._supportedDataTypes)
                    if dataType == "AnyPin":
                        if pin.optionEnabled(PinOptions.ChangeTypeOnConnection):
                            pin._supportedDataTypes = pin._defaultSupportedDataTypes
                            pin.supportedDataTypes = lambda: pin._supportedDataTypes

    def checkFree(self, checked=[], selfChek=True):
        # if self.constraint is None:
        if self.constraint is None or self.dataType == self.__class__.__name__:
            return True
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
            free = self.optionEnabled(PinOptions.ChangeTypeOnConnection)
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def allowedDataTypes(self, checked=[], dataTypes=[], selfChek=True, defaults=False):
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            return self._defaultSupportedDataTypes
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
        for port in neis + con:
            if port not in checked:
                checked.append(port)
                if not defaults:
                    dataTypes = list(set(dataTypes) & set(port._supportedDataTypes))
                else:
                    dataTypes = list(set(dataTypes) & set(port._defaultSupportedDataTypes))
                dataTypes = port.allowedDataTypes(checked,dataTypes,selfChek=True,defaults=defaults)
        return dataTypes

    def setDefault(self):
        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        self.super = AnyPin
        self.activeDataType = self.__class__.__name__

        self.call = lambda: None

        self.dataTypeBeenSet.send()

        self.setDefaultValue(None)

        self._supportedDataTypes = self._defaultSupportedDataTypes
        self.supportedDataTypes = lambda: self._supportedDataTypes

    def initType(self,dataType,initializing=False):
        if self.checkFree([]):
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, initializing))
            return True
        return False

    def setType(self, dataType):
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            return False

        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return False

        otherClass = findPinClassByType(dataType)
        self.super = otherClass
        print self.super
        self.activeDataType = dataType
        if not self.isArray():
            self.setData(getPinDefaultValueByType(self.activeDataType))
        else:
            self.setData([])
        self.setDefaultValue(self._data)

        self.color = otherClass.color
        self.dirty = True
        self.jsonEncoderClass = otherClass.jsonEncoderClass
        self.jsonDecoderClass = otherClass.jsonDecoderClass
        self.supportedDataTypes = otherClass.supportedDataTypes
        self._supportedDataTypes = otherClass.supportedDataTypes()

        self.typeChanged.send(self.activeDataType)

        return True

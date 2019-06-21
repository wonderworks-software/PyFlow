from blinker import Signal
import json
from Qt import QtGui
from nine import str

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
        # if True, setType and setDefault will work only once
        self.singleInit = False
        self.enableOptions(PinOptions.ChangeTypeOnConnection)
        self._defaultSupportedDataTypes = self._supportedDataTypes = tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])
        self.canChange = True
        self.super = None

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
        return (200, 200, 200, 255)

    @staticmethod
    def color():
        return (200, 200, 200, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'AnyPin', None

    @staticmethod
    def internalDataStructure():
        return type(None)

    @staticmethod
    def processData(data):
        return data

    def enableOptions(self, *options):
        super(AnyPin, self).enableOptions(*options)
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            self.super = AnyPin
        self.updateError([])

    def disableOptions(self, *options):
        super(AnyPin, self).disableOptions(*options)
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            self.super = AnyPin        
        self.updateError([])

    def setTypeFromData(self,data):
        for pin in [pin for pin in getAllPinClasses() if pin.IsValuePin()]:
            pType = pin.internalDataStructure()
            if type(data) == pType:
                if pin.__name__ != self.activeDataType:
                    if self.optionEnabled(PinOptions.ChangeTypeOnConnection):#self.canChangeTypeOnConection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), []):
                        traverseConstrainedPins(self, lambda x: self.updateOnConnectionCallback(x, pin.__name__, True, None))
                        self.owningNode().checkForErrors()
                break

    def updateError(self, traversed=[]):
        nodePins = set([self])
        if self.constraint:
            nodePins = set(self.owningNode().constraints[self.constraint])
        for connectedPin in getConnectedPins(self):
            if connectedPin.isAny():
                nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                if all([neighbor.activeDataType == "AnyPin",
                        neighbor.canChangeTypeOnConection([], neighbor.optionEnabled(PinOptions.ChangeTypeOnConnection), []) or not neighbor.optionEnabled(PinOptions.AllowAny)]) :
                    neighbor.setError("AnyPin Not Initialized")
                    neighbor.super = None
                else:
                    neighbor.clearError()
                    neighbor.super = AnyPin
                traversed.append(neighbor)
                neighbor.updateError(traversed)
                #neighbor.owningNode().checkForErrors()

    def setData(self, data):
        PinBase.setData(self, data)

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

        pinClass = findPinClassByType(self.activeDataType)
        try:
            self.setData(json.loads(jsonData['value'], cls=pinClass.jsonDecoderClass()))
        except:
            self.setData(self.defaultValue())

        self.updateError([])

    def pinConnected(self, other):
        super(AnyPin, self).pinConnected(other)
        self.updateError([])
        self.owningNode().checkForErrors()

    def aboutToConnect(self, other):
        if self.canChangeTypeOnConection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), []):
            dataType = other.dataType
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, False, other))
        super(AnyPin, self).aboutToConnect(other)

    def pinDisconnected(self, other):
        super(AnyPin, self).pinDisconnected(other)
        self.updateError([])
        self.owningNode().checkForErrors()

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
                if all([self.activeDataType == "AnyPin",
                        self.canChangeTypeOnConection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), []) or not self.optionEnabled(PinOptions.AllowAny)]) :
                    self.setError("AnyPin Not Initialized")
                    self.super = None
                else:
                    self.clearError()
                    self.super = AnyPin                            


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
            canChange = self.canChangeTypeOnConection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), [])                
            free = canChange
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def allowedDataTypes(self, checked=[], dataTypes=[], selfChek=True, defaults=False):
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection) and self.activeDataType == "AnyPin":
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
                dataTypes = port.allowedDataTypes(checked, dataTypes, selfChek=True, defaults=defaults)
        return dataTypes

    def setDefault(self):
        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        self.super = None
        self.activeDataType = self.__class__.__name__

        self.call = lambda: None

        self.dataTypeBeenSet.send()

        self.setDefaultValue(None)

        self._supportedDataTypes = self._defaultSupportedDataTypes
        self.supportedDataTypes = lambda: self._supportedDataTypes

    def initType(self, dataType, initializing=False):
        if self.checkFree([]):
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, initializing))
            #self.updateError([])
            self.owningNode().checkForErrors()
            self.dataBeenSet.send(self)
            return True
        return False

    def setType(self, dataType):
        if self.activeDataType == dataType:
            return True

        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection):
            return False

        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return False

        otherClass = findPinClassByType(dataType)
        if dataType != "AnyPin":
            self.super = otherClass
        else:
            self.super = None
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
        self.dataBeenSet.send(self)

        return True

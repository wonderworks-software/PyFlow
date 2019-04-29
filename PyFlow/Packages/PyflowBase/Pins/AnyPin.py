from blinker import Signal
import json

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
        self.onSetDefaultType = Signal()
        self.setDefaultValue(None)
        self._free = True
        self.isAny = True
        self.super = None
        self.activeDataType = self.__class__.__name__
        self.isArrayByDefault = False
        # if True, setType and setDefault will work only once
        self.singleInit = False

    @PinBase.dataType.getter
    def dataType(self):
        return self.activeDataType

    @staticmethod
    def isPrimitiveType():
        return False

    @staticmethod
    def supportedDataTypes():
        # TODO: Any pin should not accept execs
        # Good example of why it should be like this is addNode with any pins - we can connect exec pins to it
        # which doesn't make sense and breaks everything
        return tuple([pin.__name__ for pin in getAllPinClasses() if pin.__name__ != "ExecPin"])

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
        return 'AnyPin', ""

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        if self.activeDataType != self.dataType:
            assert(self.super is not None)
            if not self.isArray():
                data = self.super.processData(data)
            else:
                data = [self.super.processData(i) for i in data]
        self._data = data
        PinBase.setData(self, self._data)

    def serialize(self):
        dt = super(AnyPin, self).serialize()
        constrainedType = self.activeDataType
        dt['constrainedType'] = constrainedType
        if constrainedType != self.dataType:
            pinClass = findPinClassByType(constrainedType)
            # serialize with active type's encoder
            if not pinClass.isPrimitiveType():
                encodedValue = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
            else:
                encodedValue = json.dumps(self.currentData())
            dt['value'] = encodedValue
        return dt

    def pinConnected(self, other):
        self._data = getPinDefaultValueByType(other.dataType)
        self.onPinConnected.send(other)
        if other.isAny:
            self.updateOnConnection(other)

    def updateOnConnection(self, other):
        if self.constraint is None:
            self.setType(other)
            self._free = False
        else:
            if other.dataType != self.dataType:
                self._free = False
                self.setType(other)
                for p in getConnectedPins(self):
                    if p.isAny:
                        p.updateOnConnection(other)
                for pin in self.owningNode().constraints[self.constraint]:
                    if pin != self:
                        pin.setType(other, bUpdateIsArray=False)
                        pin._free = False
                        for p in getConnectedPins(pin):
                            if p.isAny:
                                p.updateOnConnection(pin)

    def pinDisconnected(self, other):
        super(AnyPin, self).pinDisconnected(other)
        if self.constraint is None:
            if not self.hasConnections():
                self.setDefault()
                self._free = True
            else:
                self.onSetDefaultType.send()
        elif not self._free:
            self._free = self.checkFree([])
            if self._free:
                self.setDefault()
                for pin in self.owningNode().constraints[self.constraint]:
                    if pin != self:
                        pin.setDefault()
                        pin._free = True
                        for pin in list(pin.affected_by) + list(pin.affects):
                            pin.pinDisconnected(other)

    def queryConstrainedPins(self):
        print("constraint", self.constraint)
        print("node constraints", self.owningNode().constraints)

    def checkFree(self, checked=[], selfChek=True):
        # if self.constraint is None:
        if self.constraint is None or self.activeDataType == "AnyPin":
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
            free = True
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def setDefault(self):
        if self.activeDataType != self.dataType and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        self.super = None
        self.activeDataType = self.__class__.__name__

        self.call = lambda: None

        self.onSetDefaultType.send()

        self.setDefaultValue(None)
        self.setAsArray(self.isArrayByDefault)

    def setType(self, other, bUpdateIsArray=True):
        if self.activeDataType != self.dataType and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        if self.activeDataType == self.dataType or self.activeDataType not in other.supportedDataTypes():
            self.super = other.__class__
            self.activeDataType = other.dataType
            self.color = other.color
            self._data = getPinDefaultValueByType(self.activeDataType)
            self.setDefaultValue(self._data)
            self.dirty = other.dirty
            self.isPrimitiveType = other.isPrimitiveType
            self.jsonEncoderClass = other.jsonEncoderClass
            self.jsonDecoderClass = other.jsonDecoderClass
            self.typeChanged.send(self.activeDataType)
            if bUpdateIsArray:
                self.setAsArray(other.isArray() | self.isArrayByDefault)

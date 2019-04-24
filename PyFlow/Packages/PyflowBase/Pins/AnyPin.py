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

    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(AnyPin, self).__init__(name, parent, dataType, direction, **kwargs)
        self.typeChanged = Signal(str)
        self.setDefaultValue(None)
        self._free = True
        self.isAny = True
        self.origSetData = self.setData
        self.super = None
        self.activeDataType = self.dataType
        self.typeChecking = False
        # if True, setType and setDefault will work only once
        self.singleInit = False

    @staticmethod
    def isPrimitiveType():
        return False

    @staticmethod
    def supportedDataTypes():
        return tuple([pin.__name__ for pin in getAllPinClasses()])

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
        if self.dataType != "AnyPin":
            if self.super is not None:
                data = self.super.processData(data)
        self._data = data
        PinBase.setData(self, self._data)

    def serialize(self, copy=False):
        dt = super(AnyPin, self).serialize(copy=copy)
        activeType = self.dataType
        dt['dataType'] = "AnyPin"
        if activeType != "AnyPin":
            pinClass = findPinClassByType(activeType)
            # serialize with active type's encoder
            if not pinClass.isPrimitiveType():
                encodedValue = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
            else:
                encodedValue = json.dumps(self.currentData())
            dt['value'] = encodedValue
        return dt

    def pinConnected(self, other):
        self.onPinConnected.send(other)
        self.updateOnConnection(other)

    def updateOnConnection(self, other):
        if self.constraint is None:
            self.setType(other)
            self._free = False
        else:
            if other.dataType != "AnyPin":
                self._free = False
                self.setType(other)
                for e in self.connections:
                    for p in [e.source()._rawPin, e.destination()._rawPin]:
                        if p != self:
                            if p.dataType == "AnyPin" and p.dataType != self.dataType:
                                p.updateOnConnection(other)
                for port in self.owningNode()._Constraints[self.constraint]:
                    if port != self:
                        port.setType(other)
                        port._free = False
                        for e in port.getWrapper()().connections:
                            for p in [e.source()._rawPin, e.destination()._rawPin]:
                                if p != port:
                                    if p.dataType == "AnyPin" and p.dataType != self.dataType:
                                        p.updateOnConnection(port)

    def pinDisconnected(self, other):
        super(AnyPin, self).pinDisconnected(other)
        if self.constraint is None:
            if not self.hasConnections():
                self.setDefault()
                self._free = True
        elif not self._free:
            self._free = self.checkFree([])
            if self._free:
                self.setDefault()
                for pin in self.owningNode()._Constraints[self.constraint]:
                    if pin != self:
                        pin.setDefault()
                        pin._free = True
                        for pin in list(pin.affected_by) + list(pin.affects):
                            pin.pinDisconnected(other)

    def checkFree(self, checked=[], selfChek=True):
        if self.constraint is None or self.dataType == "AnyPin":
            return True
        else:
            con = []
            if selfChek:
                free = not self.hasConnections()
                if not free:
                    for connection in self.connections:
                        for c in [connection.source()._rawPin, connection.destination()._rawPin]:
                            if c != self:
                                if c not in checked:
                                    con.append(c)
            else:
                free = True
                checked.append(self)
            free = True
            for port in self.owningNode()._Constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def setDefault(self):
        if self.dataType != "AnyPin" and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        self.super = None
        self.dataType = "AnyPin"

        self.call = lambda: None

        if self.getWrapper() is not None:
            self.getWrapper()().setDefault(self.defColor())

        self.setDefaultValue(None)

    def setType(self, other):
        if self.dataType != "AnyPin" and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        if self.dataType == "AnyPin" or self.dataType not in other.supportedDataTypes():
            self.super = other.__class__
            self.dataType = other.dataType
            self.color = other.color
            self._data = getPinDefaultValueByType(self.dataType)
            self.setDefaultValue(other.defaultValue())
            self.dirty = other.dirty
            self.isPrimitiveType = other.isPrimitiveType
            self.jsonEncoderClass = other.jsonEncoderClass
            self.jsonDecoderClass = other.jsonDecoderClass
            self.typeChanged.send(self.dataType)

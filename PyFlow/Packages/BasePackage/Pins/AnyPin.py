from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *
from PyFlow import getAllPinClasses
from PyFlow import CreateRawPin


class AnyPin(PinBase):
    """doc string for SgPin"""

    def __init__(self, name, parent, dataType, direction, **kwargs):
        super(AnyPin, self).__init__(name, parent, dataType, direction, **kwargs)

        self.setDefaultValue(None)
        self.supportedDataTypesList = tuple([pin.__name__ for pin in getAllPinClasses()])
        self.origDataType = "AnyPin"
        self._free = True
        self.isAny = True
        self.origSetData = self.setData
        self.super = None

    def supportedDataTypes(self):
        return self.supportedDataTypesList

    @staticmethod
    def IsValuePin():
        return True

    @staticmethod
    def defcolor():
        return (255, 255, 255, 255)

    @staticmethod
    def color():
        return (255, 255, 255, 255)

    @staticmethod
    def pinDataTypeHint():
        return 'AnyPin', ""

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        if self.dataType != "AnyPin":
            if self.super != None:
                data = self.super.processData(data)
        self._data = data
        PinBase.setData(self, self._data)

    def serialize(self):
        dt = super(AnyPin, self).serialize()
        if self.dataType != "AnyPin":
            a = CreateRawPin("", None, self.dataType, 0)
            a.setData(self._data)
            data = a.serialize()
            dt['value'] = data["value"]
            del a
        return dt

    def updateOnConnection(self, other):
        if self.constraint == None:
            self.setType(other)
            self._free = False
        else:
            if other.dataType != "AnyPin":
                self._free = False
                self.setType(other)
                for port in self.owningNode()._Constraints[self.constraint]:
                    if port != self:
                        port.setType(other)
                        port._free = False
                        for e in port.edge_list:
                            for p in [e.source()._rawPin, e.destination()._rawPin]:
                                if p != port:
                                    if p.dataType == "AnyPin" and p.dataType != self.dataType:
                                        p.updateOnConnection(port)

    def updateOnDisconnection(self):
        if self.constraint == None:
            self.setDefault()
            self._free = True
        elif not self._free:
            self._free = self.checkFree([])
            if self._free:
                self.setDefault()
                for port in self.owningNode()._Constraints[self.constraint]:
                    if port != self:
                        port.setDefault()
                        port._free = True
                        for e in port.edge_list:
                            for p in [e.source()._rawPin, e.destination()._rawPin]:
                                if p != port:
                                    p.updateOnDisconnection()

    def checkFree(self, checked=[], selfChek=True):
        if self.constraint == None or self.dataType == "AnyPin":
            return True
        else:
            con = []
            if selfChek:
                free = not self.hasConnections()
                if not free:
                    for edge in self.edge_list:
                        for c in [edge.source()._rawPin, edge.destination()._rawPin]:
                            if c != self:
                                if c not in checked:
                                    con.append(c)
            else:
                free = True
                checked.append(self)
            free = True
            for port in self.owningNode()._Constraints[self.constraint]+con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)

            return free

    def call(self):
        super(AnyPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == 'ExecPin']:
            p.call()
        # highlight wire
        for e in self.edge_list:
            e.highlight()

    def setDefault(self):
        self.super = None
        self.dataType = "AnyPin"
        self._wrapper().setDefault(self.defcolor())
        self.setDefaultValue(None)

    def setType(self, other):
        if self.dataType == "AnyPin" or self.dataType not in other.supportedDataTypes():
            self.super = other.__class__
            self.dataType = other.dataType
            self.color = other.color
            self._wrapper().setType(other.color())
            if str(type(self._data)) == "<type 'unicode'>":
                self._data = str(self._data)
            if type(self._data) != type(other._data):
                self.setData(other.defaultValue())
            self.setDefaultValue(other.defaultValue())

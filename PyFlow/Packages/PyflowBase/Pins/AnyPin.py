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
        self._free = True
        self._isAny = True
        self.super = None
        self.activeDataType = self.__class__.__name__
        # if True, setType and setDefault will work only once
        self.singleInit = False
        self.initialized = False
        self.tempInitialized = False
        self.changeTypeOnConnection = True
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
        return 'AnyPin', ""

    @staticmethod
    def processData(data):
        return data

    def setData(self, data):
        if self.activeDataType != self.__class__.__name__:
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
        if constrainedType != self.__class__.__name__:
            pinClass = findPinClassByType(constrainedType)
            # serialize with active type's encoder
            dt['value'] = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
            dt['currDataType'] = constrainedType
        return dt

    def aboutToConnect(self,other):
        if self.changeTypeOnConnection:
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, other.dataType,False,other))
        super(AnyPin, self).aboutToConnect(other)        
    def pinConnected(self, other):
        #if self.changeTypeOnConnection:
        #    traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, other.dataType,False,other))
        super(AnyPin, self).pinConnected(other)

    def updateOnConnectionCallback(self, pin, dataType,init=False,other=None):        
        free = pin.checkFree([])
        #print pin,free
        if  free:
            if (dataType == "AnyPin" and not init):#(initialize or dataType != "AnyPin"):
                return
            else :#if dataType in pin.allowedDataTypes([],pin._supportedDataTypes) or dataType == "AnyPin" or (other and not other.checkFree([],False)):
                pin.setType(dataType)
                if init:
                    pin.initialized = True
                if other:
                    pin._supportedDataTypes = other.allowedDataTypes([],other._supportedDataTypes)  
                else:
                    pin._supportedDataTypes = findPinClassByType(dataType).supportedDataTypes()                 
                if dataType == "AnyPin":
                    self._supportedDataTypes = self._defaultSupportedDataTypes
                    self.supportedDataTypes = lambda: self._supportedDataTypes
                    pin._free = True
                
               
    def updateOnDisconnectionCallback(self, pin):
        free = pin.checkFree([])
        if free:
            pin._free = True
            #pin.setDefault()
            #pin._supportedDataTypes = pin._defaultSupportedDataTypes
            #pin.supportedDataTypes = lambda: pin._supportedDataTypes

    def pinDisconnected(self, other):
        super(AnyPin, self).pinDisconnected(other)
        self.resetDefault()

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
            free = True
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def allowedDataTypes(self, checked=[], dataTypes=[],selfChek=True):
        # if self.constraint is None:
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
                dataTypes = list(set(dataTypes) & set(port._supportedDataTypes))
                dataTypes = port.allowedDataTypes(checked,dataTypes)
        return dataTypes

    def allowedDefaultDataTypes(self, checked=[], dataTypes=[],selfChek=True):
        # if self.constraint is None:
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
                dataTypes = list(set(dataTypes) & set(port._defaultSupportedDataTypes))
                dataTypes = port.allowedDataTypes(checked,dataTypes)
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
        if not self.hasConnections():
            self._free = True

        self._supportedDataTypes = self._defaultSupportedDataTypes
        self.supportedDataTypes = lambda: self._supportedDataTypes

    def initType(self,dataType,initializing=False):
        if self.checkFree([]):
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType,initializing))
            return True
        return False

    def resetDefault(self):
        if self.changeTypeOnConnection:
            traverseConstrainedPins(self, lambda pin: self.updateOnDisconnectionCallback(pin))

    def setType(self, dataType):
        if not self.changeTypeOnConnection:
            return

        if self.activeDataType != self.__class__.__name__ and self.singleInit:
            # Marked as single init. Type already been set. Skip
            return

        otherClass = findPinClassByType(dataType)
        #if self.activeDataType == self.__class__.__name__ or self.activeDataType in otherClass.supportedDataTypes():
            
        self.super = otherClass#other.__class__
        self.activeDataType = dataType#other.dataType
        self._data = getPinDefaultValueByType(self.activeDataType)
        self.setDefaultValue(self._data)

        self.color = otherClass.color
        self.dirty = True
        self.jsonEncoderClass = otherClass.jsonEncoderClass
        self.jsonDecoderClass = otherClass.jsonDecoderClass
        self.supportedDataTypes = otherClass.supportedDataTypes

        self.typeChanged.send(self.activeDataType)
        self._free = self.activeDataType == self.__class__.__name__




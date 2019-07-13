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
    """**Abstract Pin -- "AnyPin"**
    
    This Pin Type is an abstraction of Pins, it is a Pin that will act as any other defined Pin.
    This type of Pin allow to create abstract Nodes that can operate in more than one dataType.

    By default AnyPin non Initialized will be marked as error, as Pyflow can't know what is inside.
    This Error can be avoided by enabling :py:attr:`PyFlow.Core.Common.PinOptions.AllowAny`. Thas how NonTyped Lists are made.

    By default :py:attr:`PyFlow.Core.Common.PinOptions.ChangeTypeOnConnection` is enabled, and that means that it will change
    its internal dataType to the new dataType provided by connection or user Initialization. If disabled, pin will not allow changes.
    
    Is important to define a bunch of allowedDataTypes on pin creation, this will restrict what pins can be connected and what no,
    so even being a AnyPin, it can be defined to allow for example only ["FloatPin","IntPin"] so only those could be connected.

    :param self.singleInit: can be set to True, so once initialized, it will never be able to change dataType
    :param self.checkForErrors: can be set To False so it will never try to find errors
    
    Signals:
        * **typeChanged** : Fired when dataType has change
    
    """

    def __init__(self, name, owningNode, direction, **kwargs):
        """        
        :param name: Pin name
        :type name: string
        :param owningNode: Owning Node
        :type owningNode: :py:class:`PyFlow.Core.NodeBase.NodeBase`
        :param direction: PinDirection , can be input or output
        :type direction: :py:class:`PyFlow.Core.Common.PinDirection`
        """
        super(AnyPin, self).__init__(name, owningNode, direction, **kwargs)
        self.typeChanged = Signal(str)
        self.dataTypeBeenSet = Signal()
        self.setDefaultValue(None)
        self._isAny = True
        # if True, setType and setDefault will work only once
        self.singleInit = False
        self.checkForErrors = True
        self.enableOptions(PinOptions.ChangeTypeOnConnection)
        self._defaultSupportedDataTypes = self._supportedDataTypes = tuple([pin.__name__ for pin in getAllPinClasses() if pin.IsValuePin()])
        self.canChange = True
        self.super = None
        self.prevDataType = None
        self._lastError2 = None
        
    @PinBase.dataType.getter
    def dataType(self):
        return self.activeDataType

    @staticmethod
    def supportedDataTypes():
        """Tuple with all the Defined value Pin Classes
        """
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

    def setTypeFromData(self, data):
        """Initialize DataType from actual data
        
        Iterates all defined Pin and compares type(data) with Pin.internalDataStructure() to find a valid DataType

        :param data: Actual data to search Pin/dataType from
        """
        for pin in [pin for pin in getAllPinClasses() if pin.IsValuePin()]:
            pType = pin.internalDataStructure()
            if type(data) == pType:
                if pin.__name__ != self.activeDataType:
                    if self.optionEnabled(PinOptions.ChangeTypeOnConnection):
                        traverseConstrainedPins(self, lambda x: self.updateOnConnectionCallback(x, pin.__name__, True, None))
                        self.owningNode().checkForErrors()
                break

    def updateError(self, traversed=[], updateNeis=False):
        """Check is Pin dataType is "AnyPin" and if it is, checks if it can change Type on conection, and if it can, marked as error.
        Is a iterative Function that traverses connected and constrained Pins
        
        :param traversed: Current Iterated neighbours, defaults to []
        :type traversed: list, optional
        :param updateNeis: Try to update Constrained Pins parents error display, it can be slow so use carefully, defaults to False
        :type updateNeis: bool, optional
        """
        if not self.checkForErrors:
            return
        nodePins = set([self])
        if self.constraint:
            nodePins = set(self.owningNode().constraints[self.constraint])
        for connectedPin in getConnectedPins(self):
            if connectedPin.isAny():
                nodePins.add(connectedPin)
        for neighbor in nodePins:
            if neighbor not in traversed:
                if all([neighbor.activeDataType == "AnyPin",
                        neighbor.canChangeTypeOnConnection([], neighbor.optionEnabled(PinOptions.ChangeTypeOnConnection), []) or not neighbor.optionEnabled(PinOptions.AllowAny)]) :
                    neighbor.setError("AnyPin Not Initialized")
                    neighbor.super = None
                else:
                    neighbor.clearError()
                    if neighbor.activeDataType == "AnyPin":
                        neighbor.super = AnyPin
                traversed.append(neighbor)
                if neighbor.isAny():
                    neighbor.updateError(traversed, updateNeis)
                if updateNeis:
                    neighbor.owningNode().checkForErrors()

    def serialize(self):
        """Stores The data to Json
        
        Appends current value and currentDataType to default :py:func:`PyFlow.Core.PinBase.PinBase.serialize` method
        :returns: json data
        :rtype: {dict}
        """
        dt = super(AnyPin, self).serialize()
        constrainedType = self.activeDataType
        if constrainedType != self.__class__.__name__:
            pinClass = findPinClassByType(constrainedType)
            # serialize with active type's encoder
            dt['value'] = json.dumps(self.currentData(), cls=pinClass.jsonEncoderClass())
            dt['currDataType'] = constrainedType
        return dt

    def deserialize(self, jsonData):
        """Reconstruct Pin from saved jsonData

        :param jsonData: Input Json Saved data
        :type jsonData: dict
        """
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
        """Pin Connection been Made

        We update Error here to search for nonInitialized Pins in current Node, and in connected Nodes if initializing

        :param other: Pin that has been connected to this Pin.
        :type other: :py:class:`PyFlow.Core.PinBase.PinBase`
        """
        super(AnyPin, self).pinConnected(other)
        self._lastError2 = self._lastError
        self.updateError([],self.activeDataType == "AnyPin" or self.prevDataType == "AnyPin")
        self.owningNode().checkForErrors()

    def aboutToConnect(self, other):
        """Function called before real connection but after :py:func:`PyFlow.Core.Common.canConnectPins` returns True
        
        We traverse connected and constrained Pins here to search if we can change Pin dataType, and if we can we traverse again
        changing all the necesary datatypes in connected Graph Pins.

        :param other: Pin that will be connected to this Pin.
        :type other: :py:class:`PyFlow.Core.PinBase.PinBase`
        """
        if self.canChangeTypeOnConnection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), []):
            dataType = other.dataType
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, False, other))
        super(AnyPin, self).aboutToConnect(other)

    def pinDisconnected(self, other):
        """Pin has been disconnected
        
        We update error here and checkFor errors in owning Node

        :param other: Pin that has been disconected to this Pin.
        :type other: :py:class:`PyFlow.Core.PinBase.PinBase`
        """
        super(AnyPin, self).pinDisconnected(other)
        self.updateError([],self.activeDataType == "AnyPin" or self.prevDataType == "AnyPin")
        self._lastError2 = self._lastError
        if self.activeDataType == "AnyPin" and self._lastError2 == None:
            self.prevDataType = "AnyPin"
        else:
            self.prevDataType = None        
        self.owningNode().checkForErrors()

    def updateOnConnectionCallback(self, pin, dataType, init=False, other=None):
        """Method Called in traverse function :py:func:`PyFlow.Core.Common.traverseConstrainedPins`
        
        This Function is called for all the connected Pins to the initial Pin calling it. 
        Here we traverse all pins and call :py:func:`AnyPin.setType` for all of them.
        We also intersect all the connected pins allowedDataTypes.
        :param pin: Pin to perform operations on
        :type pin: :py:class:`AnyPin`
        :param dataType: New DataType to apply
        :type dataType: string
        :param init: If initializing AnyPin can have same strenght as other types, if not, "AnyPin" Pin will always be weaker than other dataType, if, defaults to False
        :type init: bool, optional
        :param other: other Pin to heredate stuff from him, defaults to None
        :type other: :py:class:`PyFlow.Core.PinBase.PinBase`, optional
        """
        free = pin.checkFree([])
        if free:
            if (dataType == "AnyPin" and not init):
                if not other:
                    return
                else:
                    if pin.dataType != "AnyPin" and pin.dataType in other.allowedDataTypes([], other._supportedDataTypes) and other.canChangeTypeOnConnection([], other.optionEnabled(PinOptions.ChangeTypeOnConnection), []):
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

    def checkFree(self, checked=[], selfCheck=True):
        """Recursive Function to find if all connected Pins are of type :py:class:`AnyPin` and canChange On conection,
        so basically it checks if a Pin is free to change its dataType to another one

        :param checked: Already visited Pins, defaults to []
        :type checked: list, optional
        :param selfCheck: Define if check Pin itself or no, this is useful when trying to override a conection that is in fact
                        the only conection that make hole graphed nodes not be able to change Type, defaults to True
        :type selfCheck: bool, optional
        :returns: True if Pin can change current dataType
        :rtype: {bool}
        """
        if self.constraint is None or self.dataType == self.__class__.__name__:
            return True
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
            canChange = self.canChangeTypeOnConnection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), [])                
            free = canChange
            for port in self.owningNode().constraints[self.constraint] + con:
                if port not in checked:
                    checked.append(port)
                    if not isinstance(port, AnyPin):
                        free = False
                    elif free:
                        free = port.checkFree(checked)
            return free

    def allowedDataTypes(self, checked=[], dataTypes=[], selfCheck=True, defaults=False):
        """Recursive Function to intersect allowedDatatypes of all connected pins.

        :param checked: Already visited Pins, defaults to []
        :type checked: list, optional
        :param dataTypes: Intersected dataTypes, defaults to []
        :type dataTypes: list, optional
        :param selfCheck: Define if check Pin itself or no, this is useful when trying to override a conection that is in fact
                        the only conection that make hole graphed nodes not be able to change Type, defaults to True
        :type selfCheck: bool, optional
        :param defaults: Define if we are intersecting current allowedDataTypes, or default (as in definition of node) allowedDataTypes, defaults to False
        :type defaults: bool, optional
        :returns: List contatining all the intersected dataTypes
        :rtype: {list}
        """
        if not self.optionEnabled(PinOptions.ChangeTypeOnConnection) and self.activeDataType == "AnyPin":
            return self._defaultSupportedDataTypes
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
        for port in neis + con:
            if port not in checked:
                checked.append(port)
                if not defaults:
                    dataTypes = list(set(dataTypes) & set(port._supportedDataTypes))
                else:
                    dataTypes = list(set(dataTypes) & set(port._defaultSupportedDataTypes))
                dataTypes = port.allowedDataTypes(checked, dataTypes, selfCheck=True, defaults=defaults)
        return dataTypes

    def initType(self, dataType, initializing=False):
        """Same as :py:func:`AnyPin.aboutToConnect` but instead of using another Pin using a dataType name
        
        :param dataType: New DataType we want the pin to became
        :type dataType: string
        :param initializing:  If initializing AnyPin can have same strenght as other types, if not, "AnyPin" Pin will always be weaker than other dataType, if, defaults to False
        :type initializing: bool, optional
        :returns: True if it can change to the asked dataType
        :rtype: {bool}
        """
        if self.canChangeTypeOnConnection([], self.optionEnabled(PinOptions.ChangeTypeOnConnection), []):
            traverseConstrainedPins(self, lambda pin: self.updateOnConnectionCallback(pin, dataType, initializing))
            self._lastError2 = self._lastError
            self.updateError([],self.activeDataType == "AnyPin" or self.prevDataType == "AnyPin")
            self.owningNode().checkForErrors()
            return True
        return False

    def setType(self, dataType):
        """Here is where :py:class:`AnyPin` heredates all the properties from other defined dataTypes and act like those
        
        :param dataType: New DataType
        :type dataType: string
        :returns: True if succes setting dataType
        :rtype: {bool}
        """
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

        if self.activeDataType == "AnyPin" and self._lastError2 == None:
            self.prevDataType = "AnyPin"
        else:
            self.prevDataType = None

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

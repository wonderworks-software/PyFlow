from PyFlow.Core.Common import *


class ISerializable(object):
    """
    Interface for serialization and deserialization
    """
    def __init__(self):
        super(ISerializable, self).__init__()

    def serialize(self, *args, **Kwargs):
        """Implements how item will be serialized

        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('serialize method of ISerializable is not implemented')

    def deserialize(self, jsonData):
        """Implements how item will be deserialized

        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('deserialize method of ISerializable is not implemented')


class IItemBase(ISerializable):
    """Base class for pins and nodes

    .. py:method:: uid
        :property:

        :getter: Unique identifier accessor

                :raises: :class:`NotImplementedError`

        :setter: Unique identifier setter

                :raises: :class:`NotImplementedError`
    """

    def __init__(self):
        super(IItemBase, self).__init__()

    def getWrapper(self):
        """Returns reference to gui wrapper if it exists

        :rtype: gui class instance or None
        """
        return None

    def setWrapper(self, wrapper):
        """Sets gui wrapper

        :param wrapper: gui class
        :type wrapper: Whatever gui class
        """
        pass

    @property
    def uid(self):
        raise NotImplementedError('uid property of IItemBase should be implemented')

    @uid.setter
    def uid(self, value):
        raise NotImplementedError('uid setter of IItemBase should be implemented')

    @uid.deleter
    def uid(self):
        raise NotImplementedError('uid property of IItemBase can not be deleted')

    def getName(self):
        """Returns item's name

        :rtype: str

        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('getName method of IItemBase is not implemented')

    def setName(self, name):
        """Sets item name

        :param name: Target name
        :type name: str
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('setName method of IItemBase is not implemented')

    def kill(self):
        """Removes item

        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('kill method of IItemBase is not implemented')


class IPin(IItemBase):
    """Pin interface
    """

    def __init__(self):
        super(IPin, self).__init__()

    @staticmethod
    def IsValuePin():
        """Defines is this pin is holding some data or not

        For example, ExecPin is not a value pin

        :rtype: bool
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('IsValuePin method of IPin is not implemented')

    @staticmethod
    def color():
        """Defines pin color

        Can be used by gui wrapper class.

        :returns: Rgba tuple
        :rtype: typle(0, 0, 0, 255)
        """
        return (255, 0, 0, 255)

    def isExec(self):
        """Is this pin executable or not

        :rtype: bool
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('isExec method of IPin is not implemented')

    def isArray(self):
        """Is this pin holds an list of values or not

        :rtype: bool
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('isArray method of IPin is not implemented')

    def isAny(self):
        """Is this pin of type Any or not

        :rtype: bool
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('isAny method of IPin is not implemented')

    @staticmethod
    def internalDataStructure():
        """Static hint of what real python type is this pin

        :rtype: object
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('internalDataStructure method of IPin is not implemented')

    @staticmethod
    def processData(data):
        """Defines how data is processed

        :returns: Processed data
        :rtype: object
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('processData method of IPin is not implemented')

    @staticmethod
    def supportedDataTypes():
        """List of supported data types

        List of data types that can be casted to this type. For example - int can support float, or vector3 can support vector4 etc.

        :rtype: list(object)
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('supportedDataTypes method of IPin is not implemented')

    def defaultValue(self):
        """Default value for this pin

        :rtype: object
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('defaultValue method of IPin is not implemented')

    def getData(self):
        """How to return data for this pin

        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('getData method of IPin is not implemented')

    def setData(self, value):
        """How to set data to pin

        :param value: Value to set
        :type value: object
        :raises NotImplementedError: If not implemented
        """
        raise NotImplementedError('setData method of IPin is not implemented')

    def call(self, *args, **kwargs):
        """How to execute. What this should do is execute `call` on another pin,
        by using this we can evaluate nodes from left to right and define control flow
        """
        pass

    @property
    def dataType(self):
        """How to return this pin data type

        :rtype: str

        :setter: How to set this pin data type
        """
        raise NotImplementedError('dataType getter method of IPin is not implemented')

    @dataType.setter
    def dataType(self, value):
        raise NotImplementedError('dataType setter method of IPin is not implemented')

    @staticmethod
    def jsonEncoderClass():
        raise NotImplementedError('jsonEncoderClass method of IPin is not implemented')

    @staticmethod
    def jsonDecoderClass():
        raise NotImplementedError('jsonEncoderClass method of IPin is not implemented')

    def setAsArray(self, bIsArray):
        raise NotImplementedError('setAsArray method of IPin is not implemented')


class INode(IItemBase):

    def __init__(self):
        super(INode, self).__init__()

    def compute(self, *args, **kwargs):
        raise NotImplementedError('compute method of INode is not implemented')

    def isCallable(self):
        raise NotImplementedError('isCallable method of INode is not implemented')

    def call(self, outPinName, *args, **kwargs):
        """call out exec pin by name
        """
        raise NotImplementedError('call method of INode is not implemented')

    def createInputPin(self, pinName, dataType, defaultValue=None, foo=None, structure=PinStructure.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):
        raise NotImplementedError('createInputPin method of INode is not implemented')

    def createOutputPin(self, pinName, dataType, defaultValue=None, structure=PinStructure.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):
        raise NotImplementedError('createOutputPin method of INode is not implemented')

    def getUniqPinName(self, name):
        raise NotImplementedError('getUniqPinName method of INode is not implemented')

    def postCreate(self, jsonTemplate=None):
        raise NotImplementedError('postCreate method of INode is not implemented')

    def setData(self, pinName, data, pinSelectionGroup):
        raise NotImplementedError('setData method of INode is not implemented')

    def getData(self, pinName, pinSelectionGroup):
        raise NotImplementedError('getData method of INode is not implemented')


class ICodeCompiler(object):
    def __init__(self, *args, **kwargs):
        super(ICodeCompiler, self).__init__(*args, **kwargs)

    def compile(self, code):
        raise NotImplementedError('compile method of ICodeCompiler is not implemented')


class IEvaluationEngine(object):
    """docstring for IEvaluationEngine."""
    def __init__(self):
        super(IEvaluationEngine, self).__init__()

    @staticmethod
    def getPinData(pin):
        raise NotImplementedError('getPinData method of IEvaluationEngine is not implemented')

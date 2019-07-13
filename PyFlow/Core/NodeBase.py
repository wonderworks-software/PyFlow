from blinker import Signal
import weakref
import functools
import uuid
import keyword
import json
from collections import OrderedDict
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec
from types import MethodType
from multipledispatch import dispatch
import collections

from PyFlow import getPinDefaultValueByType
from PyFlow import getRawNodeInstance
from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import INode
from PyFlow import CreateRawPin


class NodePinsSuggestionsHelper(object):
    """Describes node's pins types and structs for inputs and outputs
    separately. Used by nodebox to suggest good nodes.
    """
    def __init__(self):
        super(NodePinsSuggestionsHelper, self).__init__()
        self.template = {'types': {'inputs': [], 'outputs': []},
                         'structs': {'inputs': [], 'outputs': []}}
        self.inputTypes = set()
        self.outputTypes = set()
        self.inputStructs = set()
        self.outputStructs = set()

    def addInputDataType(self, dataType):
        self.inputTypes.add(dataType)

    def addOutputDataType(self, dataType):
        self.outputTypes.add(dataType)

    def addInputStruct(self, struct):
        self.inputStructs.add(struct)

    def addOutputStruct(self, struct):
        self.outputStructs.add(struct)


class NodeBase(INode):
    _packageName = ""

    def __init__(self, name, uid=None):
        super(NodeBase, self).__init__()
        self.bCacheEnabled = True
        self.cacheMaxSize = 1000
        self.cache = {}

        self.killed = Signal()
        self.tick = Signal(float)
        self.errorOccured = Signal(object)
        self.errorCleared = Signal()

        self._uid = uuid.uuid4() if uid is None else uid
        self.graph = None
        self.name = name
        self.pinsCreationOrder = OrderedDict()
        self._pins = set()
        self.x = 0.0
        self.y = 0.0
        self.bCallable = False
        self._wrapper = None
        self._constraints = {}
        self._structConstraints = {}
        self.lib = None
        self.isCompoundNode = False
        self._lastError = None
        self.__wrapperJsonData = None
        self.headerColor = None

    @property
    def wrapperJsonData(self):
        try:
            dt = self.__wrapperJsonData.copy()
            self.__wrapperJsonData.clear()
            self.__wrapperJsonData = None
            return dt
        except:
            return None

    def isValid(self):
        return self._lastError is None

    def clearError(self):
        self._lastError = None
        self.errorCleared.send()

    def setError(self, err):
        self._lastError = str(err)
        self.errorOccured.send(self._lastError)

    def checkForErrors(self):
        failedPins = {}
        for pin in self._pins:
            if pin._lastError is not None:
                failedPins[pin.name] = pin._lastError
        if len(failedPins):
            self._lastError = "Error on Pins:%s" % str(failedPins)
        else:
            self.clearError()
        wrapper = self.getWrapper()
        if wrapper:
            wrapper.update()

    @property
    def packageName(self):
        return self._packageName

    @property
    def constraints(self):
        return self._constraints

    @property
    def structConstraints(self):
        return self._structConstraints

    def getOrderedPins(self):
        return self.pinsCreationOrder.values()

    def getter(self, pinName):
        pin = self.getPinByName(pinName)
        if not pin:
            raise Exception()
        else:
            return pin

    def __getitem__(self, pinName):
        try:
            return self.getter(pinName)
        except Exception as x:
            if "<str>" in str(x):
                try:
                    return self.getter(str(pinName))
                except:
                    raise Exception("Could not find pin with name:{0}".format(pinName))
            else:
                raise Exception("Could not find signature for __getitem__:{0}".format(type(pinName)))

    @property
    def pins(self):
        return self._pins

    @property
    def inputs(self):
        """Returns all input pins. Dictionary generated every time property called, so cache it when possible.
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Input:
                result[pin.uid] = pin
        return result

    @property
    def orderedInputs(self):
        result = {}
        sortedInputs = sorted(self.inputs.values(), key=lambda x: x.pinIndex)
        for inp in sortedInputs:
            result[inp.pinIndex] = inp
        return result

    @property
    def namePinInputsMap(self):
        """Returns all input pins. Dictionary generated every time property called, so cache it when possible.
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Input:
                result[pin.name] = pin
        return result

    @property
    def outputs(self):
        """Returns all output pins. Dictionary generated every time property called, so cache it when possible.
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Output:
                result[pin.uid] = pin
        return result

    @property
    def orderedOutputs(self):
        result = {}
        sortedOutputs = sorted(self.outputs.values(), key=lambda x: x.pinIndex)
        for out in sortedOutputs:
            result[out.pinIndex] = out
        return result

    @property
    def namePinOutputsMap(self):
        """Returns all output pins. Dictionary generated every time property called, so cache it when possible.
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Output:
                result[pin.name] = pin
        return result

    # IItemBase interface

    def setWrapper(self, wrapper):
        if self._wrapper is None:
            self._wrapper = wrapper

    def getWrapper(self):
        return self._wrapper

    def location(self):
        return self.graph().location()

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self.graph is not None:
            self.graph().getNodes()[value] = self.graph().getNodes().pop(self._uid)
        self._uid = value

    @staticmethod
    def jsonTemplate():
        template = {'package': None,
                    'lib': None,
                    'type': None,
                    'owningGraphName': None,
                    'name': None,
                    'uuid': None,
                    'inputs': [],
                    'outputs': [],
                    'meta': {'var': {}},
                    'wrapper': {}
                    }
        return template

    def serialize(self):
        template = NodeBase.jsonTemplate()

        uidString = str(self.uid)
        nodeName = self.name

        template['package'] = self.packageName
        template['lib'] = self.lib
        template['type'] = self.__class__.__name__
        template['name'] = nodeName
        template['owningGraphName'] = self.graph().name
        template['uuid'] = uidString
        template['inputs'] = [i.serialize() for i in self.inputs.values()]
        template['outputs'] = [o.serialize() for o in self.outputs.values()]
        template['meta']['label'] = self.name
        template['x'] = self.x
        template['y'] = self.y

        # if running with ui get ui wrapper data to save
        wrapper = self.getWrapper()
        if wrapper:
            template['wrapper'] = wrapper.serializationHook()
        return template

    def isUnderActiveGraph(self):
        return self.graph() == self.graph().graphManager.activeGraph()

    def kill(self, *args, **kwargs):
        if self.uid not in self.graph().getNodes():
            return

        self.killed.send()

        for pin in self.inputs.values():
            pin.kill()
        for pin in self.outputs.values():
            pin.kill()
        self.graph().getNodes().pop(self.uid)

    def Tick(self, delta):
        self.tick.send(delta)

    @staticmethod
    def category():
        return "Default"

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def pinTypeHints():
        return NodePinsSuggestionsHelper()

    @staticmethod
    def description():
        return "Default node description"

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = str(name)

    def useCache(self):
        # if cached results exists - return them without calling compute
        args = tuple([pin.currentData() for pin in self.inputs.values() if pin.IsValuePin()])

        # not hashable types will not be cached
        for arg in args:
            if not isinstance(arg, collections.Hashable):
                return False

        if args in self.cache:
            for outPin, data in self.cache[args].items():
                outPin.setData(data)
            return True

    def afterCompute(self):
        if len(self.cache) >= self.cacheMaxSize:
            return

        # cache results
        args = tuple([pin.currentData() for pin in self.inputs.values() if pin.IsValuePin()])
        for arg in args:
            if not isinstance(arg, collections.Hashable):
                return

        cache = {}
        for pin in self.outputs.values():
            cache[pin] = pin.currentData()
        self.cache[args] = cache

    def processNode(self, *args, **kwargs):
        if not self.isValid():
            return
        if self.bCacheEnabled:
            if not self.useCache():
                try:
                    self.compute()
                    self.clearError()
                    self.checkForErrors()
                except Exception as e:
                    self.setError(e)
            self.afterCompute()
        else:
            try:
                self.compute()
                self.clearError()
                self.checkForErrors()
            except Exception as e:
                self.setError(e)

    # INode interface

    def compute(self, *args, **kwargs):
        """This is node's brains. Main logic goes here

        Here are basic steps:

        1. Get data from input pins
        2. Do stuff
        3. Set data to output pins
        4. Call execs if needed

        Here is compute method of charge node

        .. code-block:: python
            :linenos:

            def compute(self, *args, **kwargs):
                step = abs(self.step.getData())
                if (self._currentAmount + step) < abs(self.amount.getData()):
                    self._currentAmount += step
                    return
                self.completed.call(*args, **kwargs)
                self._currentAmount = 0.0

        .. note:: See :mod:`PyFlow.Packages.PyFlowBase.Nodes` source code module for more examples

        """
        pass

    # INode interface end

    def isCallable(self):
        """Whether this node is callable or not
        """
        for p in list(self.inputs.values()) + list(self.outputs.values()):
            if p.isExec():
                return True
        return False

    def setPosition(self, x, y):
        """Sets node coordinate on canvas

        Used to correctly restore gui wrapper class

        :param x: X coordinate
        :type x: float
        :param y: Y coordinate
        :type y: float
        """
        self.x = x
        self.y = y

    def autoAffectPins(self):
        """All value inputs affects on all value outputs. All exec inputs affects on all exec outputs
        """
        for i in self.inputs.values():
            for o in self.outputs.values():
                assert(i is not o)
                if not i.IsValuePin() and o.IsValuePin():
                    continue
                if i.IsValuePin() and not o.IsValuePin():
                    continue
                pinAffects(i, o)

    def createInputPin(self, pinName, dataType, defaultValue=None, foo=None, structure=PinStructure.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):
        """Creates input pin

        :param pinName: Pin name
        :type pinName: str
        :param dataType: Pin data type
        :type dataType: str
        :param defaultValue: Pin default value
        :type defaultValue: object
        :param foo: Pin callback. used for exec pins
        :type foo: function
        :param structure: Pin structure
        :type structure: :class:`~PyFlow.Core.Common.PinStructure.Single`
        :param constraint: Pin constraint. Should be any hashable type. We use str
        :type constraint: object
        :param structConstraint: Pin struct constraint. Also should be hashable type
        :type structConstraint: object
        :param supportedPinDataTypes: List of allowed pin data types to be connected. Used by AnyPin
        :type supportedPinDataTypes: list(str)
        :param group: Pin group. Used only by ui wrapper
        :type group: str
        """
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Input)
        p.structureType = structure
        p.group = group

        if structure == PinStructure.Array:
            p.initAsArray(True)
        elif structure == PinStructure.Dict:
            p.initAsDict(True)
        elif structure == PinStructure.Multi:
            p.enableOptions(PinOptions.ArraySupported)

        if foo:
            p.onExecute.connect(foo, weak=False)

        if defaultValue is not None or dataType == "AnyPin":
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
            if dataType == "AnyPin":
                p.setTypeFromData(defaultValue)
        else:
            p.setDefaultValue(getPinDefaultValueByType(dataType))

        if dataType == "AnyPin" and supportedPinDataTypes:
            def supportedDataTypes():
                return supportedPinDataTypes
            p._supportedDataTypes = p._defaultSupportedDataTypes = tuple(supportedPinDataTypes)
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        if structConstraint is not None:
            p.updateStructConstraint(structConstraint)
        return p

    def createOutputPin(self, pinName, dataType, defaultValue=None, structure=PinStructure.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group=""):
        """Creates output pin

        :param pinName: Pin name
        :type pinName: str
        :param dataType: Pin data type
        :type dataType: str
        :param defaultValue: Pin default value
        :type defaultValue: object
        :param structure: Pin structure
        :type structure: :class:`~PyFlow.Core.Common.PinStructure.Single`
        :param constraint: Pin constraint. Should be any hashable type. We use str
        :type constraint: object
        :param structConstraint: Pin struct constraint. Also should be hashable type
        :type structConstraint: object
        :param supportedPinDataTypes: List of allowed pin data types to be connected. Used by AnyPin
        :type supportedPinDataTypes: list(str)
        :param group: Pin group. Used only by ui wrapper
        :type group: str
        """
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Output)
        p.structureType = structure
        p.group = group

        if structure == PinStructure.Array:
            p.initAsArray(True)
        elif structure == PinStructure.Dict:
            p.initAsDict(True)
        elif structure == PinStructure.Multi:
            p.enableOptions(PinOptions.ArraySupported)

        if defaultValue is not None or dataType == "AnyPin":
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
            if dataType == "AnyPin":
                p.setTypeFromData(defaultValue)
        else:
            p.setDefaultValue(getPinDefaultValueByType(dataType))

        if dataType == "AnyPin" and supportedPinDataTypes:
            def supportedDataTypes():
                return supportedPinDataTypes
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        if structConstraint is not None:
            p.updateStructConstraint(structConstraint)
        return p

    def setData(self, pinName, data, pinSelectionGroup=PinSelectionGroup.BothSides):
        """Sets data to pin by pin name

        :param pinName: Target pin name
        :type pinName: str
        :param data: Pin data to be set
        :type data: object
        :param pinSelectionGroup: Which side to search
        :type pinSelectionGroup: :class:`~PyFlow.Core.Common.PinSelectionGroup`
        """
        p = self.getPinSG(str(pinName), pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        p.setData(data)

    def getData(self, pinName, pinSelectionGroup=PinSelectionGroup.BothSides):
        """Get data from pin by name

        :param pinName: Target pin name
        :type pinName: str
        :param pinSelectionGroup: Which side to search
        :type pinSelectionGroup: :class:`~PyFlow.Core.Common.PinSelectionGroup`
        :rtype: object
        """
        p = self.getPinSG(str(pinName), pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        return p.currentData()

    def getUniqPinName(self, name):
        """Returns unique name for pin

        :param name: Target pin name
        :type name: str
        :rtype: str
        """
        pinNames = [i.name for i in list(list(self.inputs.values())) + list(list(self.outputs.values()))]
        return getUniqNameFromList(pinNames, name)

    def __repr__(self):
        graphName = self.graph().name if self.graph is not None else str(None)
        return "<class[{0}]; name[{1}]; graph[{2}]>".format(self.__class__.__name__, self.getName(), graphName)

    def call(self, name, *args, **kwargs):
        """Call exec pin by name

        :param name: Target pin name
        :type name: str
        """
        namePinOutputsMap = self.namePinOutputsMap
        namePinInputsMap = self.namePinInputsMap
        if name in namePinOutputsMap:
            p = namePinOutputsMap[name]
            if p.isExec():
                p.call(*args, **kwargs)
        if name in namePinInputsMap:
            p = namePinInputsMap[name]
            if p.isExec():
                p.call(*args, **kwargs)

    def getPinSG(self, name, pinsSelectionGroup=PinSelectionGroup.BothSides):
        """Tries to find pin by name and selection group

        :param name: Pin name to search
        :type name: str
        :param pinsSelectionGroup: Side to search
        :type pinsSelectionGroup: :class:`~PyFlow.Core.Common.PinSelectionGroup`
        :rtype: :class:`~PyFlow.Core.PinBase.PinBase` or None
        """
        inputs = self.inputs
        outputs = self.outputs
        if pinsSelectionGroup == PinSelectionGroup.BothSides:
            for p in list(inputs.values()) + list(outputs.values()):
                if p.name == name:
                    return p
        elif pinsSelectionGroup == PinSelectionGroup.Inputs:
            for p in list(inputs.values()):
                if p.name == name:
                    return p
        else:
            for p in list(outputs.values()):
                if p.name == name:
                    return p

    def getPinByName(self, name):
        """Tries to find pin by name

        :param name: pin name
        :type name: str
        :rtype: :class:`~PyFlow.Core.PinBase.PinBase` or None
        """
        inputs = self.inputs
        outputs = self.outputs
        for p in list(inputs.values()) + list(outputs.values()):
            if p.name == name:
                return p

        if uid in inputs:
            return inputs[uid]
        if uid in outputs:
            return outputs[uid]
        return None

    def postCreate(self, jsonTemplate=None):
        """Called after node was added to graph

        :param jsonTemplate: Serialized data of spawned node
        :type jsonTemplate: dict or None
        """
        if jsonTemplate is not None:
            self.uid = uuid.UUID(jsonTemplate['uuid'])
            self.setName(jsonTemplate['name'])
            self.x = jsonTemplate['x']
            self.y = jsonTemplate['y']

            # set pins data
            sortedInputs = sorted(jsonTemplate['inputs'], key=lambda pinDict: pinDict["pinIndex"])
            for inpJson in sortedInputs:
                dynamicEnabled = PinOptions.Dynamic.value in inpJson["options"]
                if dynamicEnabled or inpJson['name'] not in self.namePinInputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPinSG(str(inpJson['name']), PinSelectionGroup.Inputs)
                pin.deserialize(inpJson)

            sortedOutputs = sorted(jsonTemplate['outputs'], key=lambda pinDict: pinDict["pinIndex"])
            for outJson in sortedOutputs:
                dynamicEnabled = PinOptions.Dynamic.value in outJson["options"]
                if dynamicEnabled or outJson['name'] not in self.namePinOutputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPinSG(str(outJson['name']), PinSelectionGroup.Outputs)
                pin.deserialize(outJson)

            # store data for wrapper
            if "wrapper" in jsonTemplate:
                self.__wrapperJsonData = jsonTemplate["wrapper"]

        if self.isCallable():
            self.bCallable = True

        # make no sense cache nodes without inputs
        if len(self.inputs) == 0:
            self.bCacheEnabled = False

        self.autoAffectPins()
        self.checkForErrors()

    @staticmethod
    def initializeFromFunction(foo):
        """Constructs node from annotated function

        .. seealso :: :mod:`PyFlow.Core.FunctionLibrary`

        :param foo: Annotated function
        :type foo: function
        :rtype: :class:`~PyFlow.Core.NodeBase.NodeBase`
        """
        retAnyOpts = None
        retConstraint = None
        foo = foo
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        returnPinOptionsToEnable = None
        returnPinOptionsToDisable = None
        returnWidgetVariant = "DefaultWidget"
        retStructConstraint = None
        if foo.__annotations__['return'] is not None:
            returnType = foo.__annotations__['return'][0]
            returnDefaultValue = foo.__annotations__['return'][1]
            if len(foo.__annotations__['return']) == 3:
                if "supportedDataTypes" in foo.__annotations__['return'][2]:
                    retAnyOpts = foo.__annotations__['return'][2]["supportedDataTypes"]
                if "constraint" in foo.__annotations__['return'][2]:
                    retConstraint = foo.__annotations__['return'][2]["constraint"]
                if "structConstraint" in foo.__annotations__['return'][2]:
                    retStructConstraint = foo.__annotations__['return'][2]["structConstraint"]
                if "enabledOptions" in foo.__annotations__['return'][2]:
                    returnPinOptionsToEnable = foo.__annotations__['return'][2]["enabledOptions"]
                if "disabledOptions" in foo.__annotations__['return'][2]:
                    returnPinOptionsToDisable = foo.__annotations__['return'][2]["disabledOptions"]
                if "inputWidgetVariant" in foo.__annotations__['return'][2]:
                    returnWidgetVariant = foo.__annotations__['return'][2]["inputWidgetVariant"]

        nodeType = foo.__annotations__['nodeType']
        _packageName = foo.__annotations__['packageName']
        libName = foo.__annotations__['lib']
        fooArgNames = getargspec(foo).args

        @staticmethod
        def description():
            return foo.__doc__

        @staticmethod
        def category():
            return meta['Category']

        @staticmethod
        def keywords():
            return meta['Keywords']

        def constructor(self, name, **kwargs):
            NodeBase.__init__(self, name, **kwargs)

        nodeClass = type(foo.__name__, (NodeBase,), {'__init__': constructor,
                                                     'category': category,
                                                     'keywords': keywords,
                                                     'description': description
                                                     })

        nodeClass._packageName = _packageName

        raw_inst = nodeClass(foo.__name__)
        raw_inst.lib = libName

        # this is list of 'references' outputs will be created for
        refs = []
        outExec = None

        # generate compute method from function
        def compute(self, *args, **kwargs):
            # arguments will be taken from inputs
            if not self.isValid():
                return
            kwds = {}
            for i in list(self.inputs.values()):
                if not i.isExec():
                    kwds[i.name] = i.getData()
            for ref in refs:
                if not ref.isExec():
                    kwds[ref.name] = ref.setData
            result = foo(**kwds)
            if returnType is not None:
                self.setData(str('out'), result)
            if nodeType == NodeTypes.Callable:
                outExec.call(*args, **kwargs)

        raw_inst.compute = MethodType(compute, raw_inst)

        if 'CacheEnabled' in meta:
            raw_inst.bCacheEnabled = meta['CacheEnabled']

        # create execs if callable
        if nodeType == NodeTypes.Callable:
            inputExec = raw_inst.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, raw_inst.compute)
            outExec = raw_inst.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
            raw_inst.bCallable = True
            raw_inst.bCacheEnabled = False

        if returnType is not None:
            p = raw_inst.createOutputPin('out', returnType, returnDefaultValue, supportedPinDataTypes=retAnyOpts, constraint=retConstraint, structConstraint=retStructConstraint)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)
            p.initAsArray(isinstance(returnDefaultValue, list))
            p.inputWidgetVariant = returnWidgetVariant
            if returnPinOptionsToEnable is not None:
                p.enableOptions(returnPinOptionsToEnable)
            if returnPinOptionsToDisable is not None:
                p.disableOptions(returnPinOptionsToDisable)
            if not p.isArray() and p.optionEnabled(PinOptions.ArraySupported):
                p.structureType = PinStructure.Multi
            elif p.isArray():
                p.structureType = PinStructure.Array

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            argName = fooArgNames[index]
            pinDescriptionTuple = foo.__annotations__[argName]
            anyOpts = None
            constraint = None
            structConstraint = None
            pinOptionsToEnable = None
            pinOptionsToDisable = None
            inputWidgetVariant = "DefaultWidget"
            # tuple means this is reference pin with default value eg - (dataType, defaultValue)
            if str("Reference") == pinDescriptionTuple[0]:
                pinDataType = pinDescriptionTuple[1][0]
                pinDefaultValue = pinDescriptionTuple[1][1]
                pinDict = None
                if len(pinDescriptionTuple[1]) == 3:
                    pinDict = pinDescriptionTuple[1][2]

                if pinDict is not None:
                    if "supportedDataTypes" in pinDict:
                        anyOpts = pinDict["supportedDataTypes"]
                    if "constraint" in pinDict:
                        constraint = pinDict["constraint"]
                    if "structConstraint" in pinDict:
                        structConstraint = pinDict["structConstraint"]
                    if "enabledOptions" in pinDict:
                        pinOptionsToEnable = pinDict["enabledOptions"]
                    if "disabledOptions" in pinDict:
                        pinOptionsToDisable = pinDict["disabledOptions"]
                    if "inputWidgetVariant" in pinDict:
                        inputWidgetVariant = pinDict["inputWidgetVariant"]

                outRef = raw_inst.createOutputPin(argName, pinDataType, supportedPinDataTypes=anyOpts, constraint=constraint, structConstraint=structConstraint)
                outRef.initAsArray(isinstance(pinDefaultValue, list))
                outRef.setDefaultValue(pinDefaultValue)
                outRef.setData(pinDefaultValue)
                outRef.inputWidgetVariant = inputWidgetVariant
                if pinOptionsToEnable is not None:
                    outRef.enableOptions(pinOptionsToEnable)
                if pinOptionsToDisable is not None:
                    outRef.disableOptions(pinOptionsToDisable)
                if not outRef.isArray() and outRef.optionEnabled(PinOptions.ArraySupported):
                    outRef.structureType = PinStructure.Multi
                elif outRef.isArray():
                    outRef.structureType = PinStructure.Array
                refs.append(outRef)
            else:
                pinDataType = pinDescriptionTuple[0]
                pinDefaultValue = pinDescriptionTuple[1]
                pinDict = None
                if len(pinDescriptionTuple) == 3:
                    pinDict = pinDescriptionTuple[2]

                if pinDict is not None:
                    if "supportedDataTypes" in pinDict:
                        anyOpts = pinDict["supportedDataTypes"]
                    if "constraint" in pinDict:
                        constraint = pinDict["constraint"]
                    if "structConstraint" in pinDict:
                        structConstraint = pinDict["structConstraint"]
                    if "enabledOptions" in pinDict:
                        pinOptionsToEnable = pinDict["enabledOptions"]
                    if "disabledOptions" in pinDict:
                        pinOptionsToDisable = pinDict["disabledOptions"]
                    if "inputWidgetVariant" in pinDict:
                        inputWidgetVariant = pinDict["inputWidgetVariant"]

                inp = raw_inst.createInputPin(argName, pinDataType, supportedPinDataTypes=anyOpts, constraint=constraint, structConstraint=structConstraint)
                inp.initAsArray(isinstance(pinDefaultValue, list))
                inp.setData(pinDefaultValue)
                inp.setDefaultValue(pinDefaultValue)
                inp.inputWidgetVariant = inputWidgetVariant
                if pinOptionsToEnable is not None:
                    inp.enableOptions(pinOptionsToEnable)
                if pinOptionsToDisable is not None:
                    inp.disableOptions(pinOptionsToDisable)
                if not inp.isArray() and inp.optionEnabled(PinOptions.ArraySupported):
                    inp.structureType = PinStructure.Multi
                elif inp.isArray():
                    inp.structureType = PinStructure.Array
        raw_inst.autoAffectPins()
        return raw_inst

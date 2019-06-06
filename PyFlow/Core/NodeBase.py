from blinker import Signal
import weakref
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

from PyFlow import getPinDefaultValueByType
from PyFlow import getRawNodeInstance
from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import INode
from PyFlow import CreateRawPin


class NodeBase(INode):
    _packageName = ""

    def __init__(self, name, uid=None):
        super(NodeBase, self).__init__()
        # memo
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
        failed = False
        error = None
        for pin in self._pins:
            if not failed:
                if pin._lastError != None:
                    failed = True
                    error = pin._lastError
                else:
                    failed = False
                    error = None
        if failed:
            self.setError(error)
        else:
            self.clearError()
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

    @dispatch(str)
    def __getitem__(self, pinName):
        return self.getPin(pinName)

    @property
    def pins(self):
        return self._pins

    @property
    def inputs(self):
        """Returns all input pins. Dictionary generated every time property called, so cache it when possible
        Returns:
            dict(uuid: PinBase)
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Input:
                result[pin.uid] = pin
        return result

    @property
    def namePinInputsMap(self):
        """Returns all input pins. Dictionary generated every time property called, so cache it when possible
        Returns:
            dict(str: PinBase)
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Input:
                result[pin.name] = pin
        return result

    @property
    def outputs(self):
        """Returns all output pins. Dictionary generated every time property called, so cache it when possible
        Returns:
            dict(uuid: PinBase)
        """
        result = OrderedDict()
        for pin in self.pins:
            if pin.direction == PinDirection.Output:
                result[pin.uid] = pin
        return result

    @property
    def namePinOutputsMap(self):
        """Returns all output pins. Dictionary generated every time property called, so cache it when possible
        Returns:
            dict(str: PinBase)
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

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self.graph is not None:
            self.graph().nodes[value] = self.graph().nodes.pop(self._uid)
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
        if self.uid not in self.graph().nodes:
            # already killed
            # this block executes for variable getter/setter
            return

        self.killed.send()

        for pin in self.inputs.values():
            pin.kill()
        for pin in self.outputs.values():
            pin.kill()
        self.graph().nodes.pop(self.uid)

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
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def description():
        return "Default node description"

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = self.graph().graphManager.getUniqNodeName(str(name))

    def useCache(self):
        # if cached results exists - return them without calling compute
        args = tuple([pin.currentData() for pin in self.inputs.values()])
        try:
            # mutable unhashable types will not be cached
            if args in self.cache:
                for outPin, data in self.cache[args].items():
                    outPin.setData(data)
                return True
        except:
            return False

    def afterCompute(self):
        if len(self.cache) >= self.cacheMaxSize:
            return

        # cache results
        args = tuple([pin.currentData() for pin in self.inputs.values()])
        try:
            # mutable unhashable types will not be cached
            if args in self.cache:
                return
        except:
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
                except Exception as e:
                    self.setError(e)
            self.afterCompute()
        else:
            self.compute()

    # INode interface

    def compute(self, *args, **kwargs):
        '''
        node calculations here
        '''
        # getting data from inputs

        # do stuff

        # write data to outputs
        return

    # INode interface end

    def isCallable(self):
        for p in list(self.inputs.values()) + list(self.outputs.values()):
            if p.isExec():
                return True
        return False

    def setPosition(self, x, y):
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

    def createInputPin(self, pinName, dataType, defaultValue=None, foo=None, structure=PinStructure.Single, constraint=None, structConstraint=None, allowedPins=[], group=""):
        # check unique name
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Input)
        p.structureType = structure
        p.group = group

        if structure == PinStructure.Array:
            p.initAsArray(True)
        elif structure == PinStructure.Multi:
            p.enableOptions(PinOptions.ArraySupported)

        if foo:
            p.onExecute.connect(foo, weak=False)

        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        else:
            p.setDefaultValue(getPinDefaultValueByType(dataType))

        if dataType == "AnyPin" and allowedPins:
            def supportedDataTypes():
                return allowedPins
            p._supportedDataTypes = p._defaultSupportedDataTypes = tuple(allowedPins)
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        if structConstraint is not None:
            p.updatestructConstraint(structConstraint)
        return p

    def createOutputPin(self, pinName, dataType, defaultValue=None, structure=PinStructure.Single, constraint=None, structConstraint=None, allowedPins=[], group=""):
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Output)
        p.structureType = structure
        p.group = group

        if structure == PinStructure.Array:
            p.initAsArray(True)
        elif structure == PinStructure.Multi:
            p.enableOptions(PinOptions.ArraySupported)

        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        else:
            p.setDefaultValue(getPinDefaultValueByType(dataType))

        if dataType == "AnyPin" and allowedPins:
            def supportedDataTypes():
                return allowedPins
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        if structConstraint is not None:
            p.updatestructConstraint(structConstraint)
        return p

    def setData(self, pinName, data, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPin(str(pinName), pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        p.setData(data)

    def getData(self, pinName, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPin(str(pinName), pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        return p.currentData()

    def getUniqPinName(self, name):
        pinNames = [i.name for i in list(list(self.inputs.values())) + list(list(self.outputs.values()))]
        return getUniqNameFromList(pinNames, name)

    def __repr__(self):
        graphName = self.graph().name if self.graph is not None else str(None)
        return "<class[{0}]; name[{1}]; graph[{2}]>".format(self.__class__.__name__, self.getName(), graphName)

    def call(self, name, *args, **kwargs):
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

    @dispatch(str, PinSelectionGroup)
    def getPin(self, name, pinsSelectionGroup=PinSelectionGroup.BothSides):
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

    @dispatch(str)
    def getPin(self, name):
        inputs = self.inputs
        outputs = self.outputs
        for p in list(inputs.values()) + list(outputs.values()):
            if p.name == name:
                return p

    @dispatch(uuid.UUID)
    def getPin(self, uid):
        inputs = self.inputs
        outputs = self.outputs

        if uid in inputs:
            return inputs[uid]
        if uid in outputs:
            return outputs[uid]
        return None

    def postCreate(self, jsonTemplate=None):
        if jsonTemplate is not None:
            self.uid = uuid.UUID(jsonTemplate['uuid'])
            self.setName(jsonTemplate['name'])
            self.x = jsonTemplate['x']
            self.y = jsonTemplate['y']

            # set pins data
            for inpJson in jsonTemplate['inputs']:
                dynamicEnabled = PinOptions.Dynamic.value in inpJson["options"]
                if dynamicEnabled or inpJson['name'] not in self.namePinInputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPin(str(inpJson['name']), PinSelectionGroup.Inputs)
                pin.deserialize(inpJson)

            for outJson in jsonTemplate['outputs']:
                dynamicEnabled = PinOptions.Dynamic.value in outJson["options"]
                if dynamicEnabled or outJson['name'] not in self.namePinOutputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPin(str(outJson['name']), PinSelectionGroup.Outputs)
                pin.deserialize(outJson)

            # store data for wrapper
            if "wrapper" in jsonTemplate:
                self.__wrapperJsonData = jsonTemplate["wrapper"]

        if self.isCallable():
            self.bCallable = True

        self.autoAffectPins()

    @staticmethod
    # Constructs a node from given annotated function
    def initializeFromFunction(foo):
        retAnyOpts = None
        retConstraint = None
        foo = foo
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        returnPinOptionsToEnable = None
        returnPinOptionsToDisable = None
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
            p = raw_inst.createOutputPin('out', returnType, returnDefaultValue, allowedPins=retAnyOpts, constraint=retConstraint, structConstraint=retStructConstraint)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)
            p.initAsArray(isinstance(returnDefaultValue, list))
            if returnPinOptionsToEnable is not None:
                p.enableOptions(returnPinOptionsToEnable)
            if returnPinOptionsToDisable is not None:
                p.disableOptions(returnPinOptionsToDisable)
            if not p.isArray() and p.optionEnabled(PinOptions.ArraySupported):
                p.structureType = PinStructure.Multi

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            argName = fooArgNames[index]
            pinDescriptionTuple = foo.__annotations__[argName]
            anyOpts = None
            constraint = None
            structConstraint = None
            pinOptionsToEnable = None
            pinOptionsToDisable = None
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

                outRef = raw_inst.createOutputPin(argName, pinDataType, allowedPins=anyOpts, constraint=constraint, structConstraint=structConstraint)
                outRef.initAsArray(isinstance(pinDefaultValue, list))
                outRef.setDefaultValue(pinDefaultValue)
                outRef.setData(pinDefaultValue)
                if pinOptionsToEnable is not None:
                    outRef.enableOptions(pinOptionsToEnable)
                if pinOptionsToDisable is not None:
                    outRef.disableOptions(pinOptionsToDisable)
                if not outRef.isArray() and outRef.optionEnabled(PinOptions.ArraySupported):
                    outRef.structureType = PinStructure.Multi
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

                inp = raw_inst.createInputPin(argName, pinDataType, allowedPins=anyOpts, constraint=constraint, structConstraint=structConstraint)
                inp.initAsArray(isinstance(pinDefaultValue, list))
                inp.setData(pinDefaultValue)
                inp.setDefaultValue(pinDefaultValue)
                if pinOptionsToEnable is not None:
                    inp.enableOptions(pinOptionsToEnable)
                if pinOptionsToDisable is not None:
                    inp.disableOptions(pinOptionsToDisable)
                if not inp.isArray() and inp.optionEnabled(PinOptions.ArraySupported):
                    inp.structureType = PinStructure.Multi

        raw_inst.autoAffectPins()
        return raw_inst

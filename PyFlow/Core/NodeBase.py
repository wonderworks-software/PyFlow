from nine import str
from blinker import Signal
import weakref
import uuid
import keyword
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
        self.killed = Signal()
        self.tick = Signal(float)

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
        self.lib = None
        self.isCompoundNode = False

    @property
    def packageName(self):
        return self._packageName

    @property
    def constraints(self):
        return self._constraints

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
        self.name = name

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

    def createInputPin(self, pinName, dataType, defaultValue=None, foo=None, constraint=None, allowedPins=[]):
        if dataType == 'ExecPin':
            assert(foo is not None), "Invalid parameters for input exec pin. Call function must be specified"

        # check unique name
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Input)
        p.direction = PinDirection.Input
        if foo:
            # p.call = foo
            p.onExecute.connect(foo, weak=False)
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        if dataType == "AnyPin" and allowedPins:
            def supportedDataTypes():
                return allowedPins
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        return p

    def createOutputPin(self, pinName, dataType, defaultValue=None, foo=None, constraint=None, allowedPins=[]):
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Output)
        if foo:
            # p.call = foo
            p.onExecute.connect(foo, weak=False)
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        if dataType == "AnyPin" and allowedPins:
            def supportedDataTypes():
                return allowedPins
            p.supportedDataTypes = supportedDataTypes
        if constraint is not None:
            p.updateConstraint(constraint)
        return p

    def setData(self, pinName, data, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPin(pinName, pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        p.setData(data)

    def getData(self, pinName, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPin(pinName, pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        return p.getData()

    def getUniqPinName(self, name):
        pinNames = [i.name for i in list(list(self.inputs.values())) + list(list(self.outputs.values()))]
        return getUniqNameFromList(pinNames, name)

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
                if inpJson['dynamic'] or inpJson['name'] not in self.namePinInputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPin(inpJson['name'], PinSelectionGroup.Inputs)
                pin.uid = uuid.UUID(inpJson['uuid'])
                pin.setData(inpJson['value'])
                if inpJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

            for outJson in jsonTemplate['outputs']:
                if outJson['dynamic'] or outJson['name'] not in self.namePinOutputsMap:
                    # create custom dynamically created pins in derived classes
                    continue

                pin = self.getPin(outJson['name'], PinSelectionGroup.Outputs)
                pin.uid = uuid.UUID(outJson['uuid'])
                pin.setData(outJson['value'])
                if outJson['bDirty']:
                    pin.setDirty()
                else:
                    pin.setClean()

        if self.isCallable():
            self.bCallable = True

        self.autoAffectPins()

    def updateConstraints(self):
        self._constraints = {}
        for pin in self.inputs.values() + self.outputs.values():
            if pin.constraint is not None:
                if pin.constraint in self._constraints:
                    self._constraints[pin.constraint].append(pin)
                else:
                    self._constraints[pin.constraint] = [pin]

    @staticmethod
    # Constructs a node from given annotated function
    def initializeFromFunction(foo):
        retAnyOpts = None
        retConstraint = None
        foo = foo
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        if foo.__annotations__['return'] is not None:
            returnType = foo.__annotations__['return'][0]
            returnDefaultValue = foo.__annotations__['return'][1]
            if len(foo.__annotations__['return']) > 2:
                if "supportedDataTypes" in foo.__annotations__['return'][2]:
                    retAnyOpts = foo.__annotations__['return'][2]["supportedDataTypes"]
                if "constraint" in foo.__annotations__['return'][2]:
                    retConstraint = foo.__annotations__['return'][2]["constraint"]

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
        if returnType is not None:
            p = raw_inst.createOutputPin('out', returnType, returnDefaultValue, allowedPins=retAnyOpts, constraint=retConstraint)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)

        # this is array of 'references' outputs will be created for
        refs = []
        outExec = None

        # generate compute method from function
        def compute(self, *args, **kwargs):
            # arguments will be taken from inputs
            kwds = {}
            for i in list(self.inputs.values()):
                if not i.isExec():
                    kwds[i.name] = i.getData()
            for ref in refs:
                if not ref.isExec():
                    kwds[ref.name] = ref.setData
            result = foo(**kwds)
            if returnType is not None:
                self.setData('out', result)
            if nodeType == NodeTypes.Callable:
                outExec.call(*args, **kwargs)

        raw_inst.compute = MethodType(compute, raw_inst)

        # create execs if callable
        if nodeType == NodeTypes.Callable:
            inputExec = raw_inst.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, raw_inst.compute)
            outExec = raw_inst.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin', None)
            raw_inst.bCallable = True

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            argName = fooArgNames[index]
            argDefaultValue = foo.__defaults__[index]
            dataType = foo.__annotations__[argName]
            anyOpts = None
            constraint = None
            if isinstance(dataType, list):
                if dataType[0][0] == "AnyPin" and len(dataType[0]) > 2:
                    if "supportedDataTypes" in dataType[0][2]:
                        anyOpts = dataType[0][2]["supportedDataTypes"]
                    if "constraint" in dataType[0][2]:
                        constraint = dataType[0][2]["constraint"]
                dataType = dataType[0][0]
            # tuple means this is reference pin with default value eg - (dataType, defaultValue)
            if isinstance(dataType, tuple):
                if dataType[0] == "AnyPin" and len(dataType) > 2:
                    if "supportedDataTypes" in dataType[2]:
                        anyOpts = dataType[2]["supportedDataTypes"]
                    if "constraint" in dataType[2]:
                        constraint = dataType[2]["constraint"]
                outRef = raw_inst.createOutputPin(argName, dataType[0], allowedPins=anyOpts, constraint=constraint)
                outRef.setAsArray(isinstance(argDefaultValue, list))
                if outRef.isArray():
                    outRef.isArrayByDefault = True
                    outRef.supportsOnlyArray = True
                outRef.setDefaultValue(argDefaultValue)
                outRef.setData(dataType[1])
                refs.append(outRef)
            else:
                inp = raw_inst.createInputPin(argName, dataType, allowedPins=anyOpts, constraint=constraint)
                inp.setAsArray(isinstance(argDefaultValue, list))
                if inp.isArray():
                    inp.isArrayByDefault = True
                    inp.supportsOnlyArray = True
                inp.setData(argDefaultValue)
                inp.setDefaultValue(argDefaultValue)

        raw_inst.autoAffectPins()
        return raw_inst

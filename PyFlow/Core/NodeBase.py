import weakref
import uuid
import keyword
from collections import OrderedDict
try:
    from inspect import getfullargspec as getargspec
except:
    from inspect import getargspec
from types import MethodType

from PyFlow.Core.AGraphCommon import *
from PyFlow.Core.Interfaces import INode
from PyFlow import CreateRawPin


class NodeBase(INode):
    def __init__(self, name):
        super(NodeBase, self).__init__()
        self._uid = uuid.uuid4()
        self.graph = None
        self.name = name
        self.inputs = OrderedDict()
        self.namePinInputsMap = OrderedDict()
        self.outputs = OrderedDict()
        self.namePinOutputsMap = OrderedDict()
        self.x = 0.0
        self.y = 0.0
        self.bCallable = False
        self._wrapper = None
        self._Constraints = {}

    # IItemBase interface

    def setWrapper(self, wrapper):
        self._wrapper = weakref.ref(wrapper)

    def getWrapper(self):
        return self._wrapper

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self._uid in self.graph().nodes:
            self.graph().nodes[value] = self.graph().nodes.pop(self._uid)
            self._uid = value

    @staticmethod
    def jsonTemplate():
        template = {'package': None,
                    'type': None,
                    'name': None,
                    'uuid': None,
                    'inputs': [],
                    'outputs': [],
                    'meta': {'var': {}}
                    }
        return template

    def serialize(self):
        template = NodeBase.jsonTemplate()
        template['package'] = self.packageName()
        template['type'] = self.__class__.__name__
        template['name'] = self.name
        template['uuid'] = str(self.uid)
        template['inputs'] = [i.serialize() for i in self.inputs.values()]
        template['outputs'] = [o.serialize() for o in self.outputs.values()]
        template['meta']['label'] = self.name
        return template

    def kill(self):
        assert(self.uid in self.graph().nodes), "Error killing node. \
            Node {0} not in graph".format(self.getName())
        self.graph().nodes.pop(self.uid)

    def Tick(self, delta):
        pass

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

    def compute(self):
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
            if p.dataType == 'ExecPin':
                return True
        return False

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def addInputPin(self, pinName, dataType, defaultValue=None, foo=None,constraint=None,allowedPins=[]):
        # check unique name
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Input)
        self.inputs[p.uid] = p
        self.namePinInputsMap[pinName] = p
        p.direction = PinDirection.Input
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        if dataType == "AnyPin" and allowedPins:
            p.supportedDataTypesList = allowedPins
        if constraint != None:
            p.updateConstraint(constraint)           
        return p

    def addOutputPin(self, pinName, dataType, defaultValue=None, foo=None,constraint=None,allowedPins=[]):
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Output)
        self.outputs[p.uid] = p
        self.namePinOutputsMap[pinName] = p
        p.direction = PinDirection.Output
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        if dataType == "AnyPin" and allowedPins:
            p.supportedDataTypesList = allowedPins            
        if constraint != None:
            p.updateConstraint(constraint)             
        return p

    def setData(self, pinName, data, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPinByName(pinName, pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        p.setData(data)

    def getData(self, pinName, pinSelectionGroup=PinSelectionGroup.BothSides):
        p = self.getPinByName(pinName, pinSelectionGroup)
        assert(p is not None), "Failed to find pin by name: {}".format(pinName)
        return p.getData()

    def getUniqPinName(self, name):
        pinNames = [i.name for i in list(list(self.inputs.values())) + list(list(self.outputs.values()))] + dir(self)
        if name not in pinNames:
            return name
        idx = 0
        tmp = name
        while tmp in pinNames:
            idx += 1
            tmp = name + str(idx)
        return name + str(idx)

    def getPinByUUID(self, uid):
        if uid in self.inputs:
            return self.inputs[uid]
        if uid in self.outputs:
            return self.outputs[uid]
        return None

    def getPinByName(self, name, pinsSelectionGroup=PinSelectionGroup.BothSides):
        if pinsSelectionGroup == PinSelectionGroup.BothSides:
            for p in list(self.inputs.values()) + list(self.outputs.values()):
                if p.name == name:
                    return p
        elif pinsSelectionGroup == PinSelectionGroup.Inputs:
            for p in list(self.inputs.values()):
                if p.name == name:
                    return p
        else:
            for p in list(self.outputs.values()):
                if p.name == name:
                    return p

    def postCreate(self, jsonTemplate=None):
        if self.isCallable():
            self.bCallable = True

    def updateConstraints(self):
        self._Constraints = {}
        for pin in self.inputs.values() + self.outputs.values():
            if pin.constraint != None:
                if self._Constraints.has_key(pin.constraint):
                    self._Constraints[pin.constraint].append(pin)
                else:
                    self._Constraints[pin.constraint] = [pin]
    @staticmethod
    ## Constructs a node from given annotated function
    def initializeFromFunction(foo):
        retAnyOpts = None
        retConstraint = None        
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        if foo.__annotations__['return'] is not None:
            returnType = foo.__annotations__['return'][0]
            returnDefaultValue =  foo.__annotations__['return'][1]
            if len(foo.__annotations__['return'])>2:
                if foo.__annotations__['return'][2].has_key("supportedDataTypes"):
                    retAnyOpts = foo.__annotations__['return'][2]["supportedDataTypes"]
                if foo.__annotations__['return'][2].has_key("constraint"):
                    retConstraint = foo.__annotations__['return'][2]["constraint"]

        nodeType = foo.__annotations__['nodeType']
        _packageName = foo.__annotations__['packageName']
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

        @staticmethod
        def packageName():
            return _packageName

        def constructor(self, name, **kwargs):
            NodeBase.__init__(self, name, **kwargs)

        nodeClass = type(foo.__name__, (NodeBase,), {'__init__': constructor,
                                                     'category': category,
                                                     'keywords': keywords,
                                                     'description': description,
                                                     'packageName': packageName
                                                     })

        raw_inst = nodeClass(foo.__name__)

        if returnType is not None:
            p = raw_inst.addOutputPin('out', returnType, returnDefaultValue,allowedPins=retAnyOpts,constraint=retConstraint)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)

        # this is array of 'references' outputs will be created for
        refs = []
        outExec = None

        # generate compute method from function
        def compute(self):
            # arguments will be taken from inputs
            kwargs = {}
            for i in list(self.inputs.values()):
                if i.dataType is not 'ExecPin':
                    kwargs[i.name] = i.getData()
            for ref in refs:
                if ref.dataType is not 'ExecPin':
                    kwargs[ref.name] = ref.setData
            result = foo(**kwargs)
            if returnType is not None:
                self.setData('out', result)
            if nodeType == NodeTypes.Callable:
                outExec.call()

        raw_inst.compute = MethodType(compute, raw_inst)

        # create execs if callable
        if nodeType == NodeTypes.Callable:
            inputExec = raw_inst.addInputPin('inExec', 'ExecPin', None, raw_inst.compute)
            outExec = raw_inst.addOutputPin('outExec', 'ExecPin', None)
            raw_inst.bCallable = True

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            argName = fooArgNames[index]
            argDefaultValue = foo.__defaults__[index]
            dataType = foo.__annotations__[argName]
            anyOpts = None
            constraint = None  
            if isinstance(dataType, list):
                if dataType[0][0] == "AnyPin" and len(dataType[0])>2:
                    if dataType[0][2].has_key("supportedDataTypes"):
                        anyOpts = dataType[0][2]["supportedDataTypes"]
                    if dataType[0][2].has_key("constraint"):
                        constraint = dataType[0][2]["constraint"]                        
                dataType = dataType[0][0]
            # tuple means this is reference pin with default value eg - (dataType, defaultValue)
            if isinstance(dataType, tuple):
                if dataType[0] == "AnyPin" and len(dataType)>2:
                    if dataType[2].has_key("supportedDataTypes"):
                        anyOpts = dataType[2]["supportedDataTypes"]
                    if dataType[2].has_key("constraint"):
                        constraint = dataType[2]["constraint"]                 
                outRef = raw_inst.addOutputPin(argName, dataType[0],allowedPins=anyOpts,constraint=constraint)
                outRef.setDefaultValue(argDefaultValue)
                outRef.setData(dataType[1])
                if PROPAGATE_DIRTY in meta:
                    if argName in meta[PROPAGATE_DIRTY]:
                        outRef.setAlwaysPushDirty(True)
                refs.append(outRef)
            else:
                inp = raw_inst.addInputPin(argName, dataType,allowedPins=anyOpts,constraint=constraint)
                inp.setData(argDefaultValue)
                inp.setDefaultValue(argDefaultValue)
                if PROPAGATE_DIRTY in meta:
                    if argName in meta[PROPAGATE_DIRTY]:
                        inp.setAlwaysPushDirty(True)

        # all value inputs affects on all value outputs
        # all exec inputs affects on all exec outputs
        for i in raw_inst.inputs.values():
            for o in raw_inst.outputs.values():
                if i.dataType == 'ExecPin' and o.dataType != 'ExecPin':
                    continue
                if i.dataType != 'ExecPin' and o.dataType == 'ExecPin':
                    continue
                pinAffects(i, o)
        return raw_inst

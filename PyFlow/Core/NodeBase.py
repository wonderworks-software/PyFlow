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
    def __init__(self, name, graph):
        super(NodeBase, self).__init__()
        self._uid = uuid.uuid4()
        self.graph = weakref.ref(graph)
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.x = 0.0
        self.y = 0.0
        self.bCallable = False

    # IItemBase interface

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self._uid in self.graph().nodes:
            self.graph().nodes[value] = self.graph().nodes.pop(self._uid)
            self._uid = value

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

    def addInputPin(self, pinName, dataType, defaultValue=None, foo=None):
        # check unique name
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Input)
        self.inputs[p.uid] = p
        self.graph().pins[p.uid] = p
        p.direction = PinDirection.Input
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        return p

    def addOutputPin(self, pinName, dataType, defaultValue=None, foo=None):
        pinName = self.getUniqPinName(pinName)
        p = CreateRawPin(pinName, self, dataType, PinDirection.Output)
        self.outputs[p.uid] = p
        self.graph().pins[p.uid] = p
        p.direction = PinDirection.Output
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
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

    @staticmethod
    ## Constructs a node from given annotated function
    def initializeFromFunction(foo, graph):
        meta = foo.__annotations__['meta']
        returnType = returnDefaultValue = None
        if foo.__annotations__['return'] is not None:
            returnType, returnDefaultValue = foo.__annotations__['return']
        nodeType = foo.__annotations__['nodeType']
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

        def constructor(self, name, graph, **kwargs):
            NodeBase.__init__(self, name, graph, **kwargs)

        nodeClass = type(foo.__name__, (NodeBase,), {'__init__': constructor,
                                                     'category': category,
                                                     'keywords': keywords,
                                                     'description': description
                                                     })

        raw_inst = nodeClass(graph.getUniqNodeName(foo.__name__), graph)

        if returnType is not None:
            p = raw_inst.addOutputPin('out', returnType, returnDefaultValue)
            p.setData(returnDefaultValue)
            p.setDefaultValue(returnDefaultValue)
            graph.pins[p.uid] = p

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

        # iterate over function arguments and create pins according to data types
        for index in range(len(fooArgNames)):
            argName = fooArgNames[index]
            argDefaultValue = foo.__defaults__[index]
            dataType = foo.__annotations__[argName]
            # tuple means this is reference pin with default value eg - (dataType, defaultValue)
            if isinstance(dataType, tuple):
                outRef = raw_inst.addOutputPin(argName, dataType[0])
                graph.pins[outRef.uid] = outRef
                outRef.setDefaultValue(argDefaultValue)
                outRef.setData(dataType[1])
                refs.append(outRef)
            else:
                inp = raw_inst.addInputPin(argName, dataType)
                graph.pins[inp.uid] = inp
                inp.setData(argDefaultValue)
                inp.setDefaultValue(argDefaultValue)

        # all inputs affects on all outputs
        for i in raw_inst.inputs.values():
            for o in raw_inst.outputs.values():
                pinAffects(i, o)

        return raw_inst

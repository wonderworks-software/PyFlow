from AGraphCommon import *
import weakref
import uuid
import inspect
import keyword
from collections import OrderedDict
import itertools
from copy import deepcopy


class ISerializable(object):
    """
    Interface for serialization and deserialization.
    """
    def __init__(self):
        super(ISerializable, self).__init__()

    def serialize(self, *args, **Kwargs):
        '''
        Implements how item should be serialized.

        Raises:
            NotImplementedError.
        '''
        raise NotImplementedError('serialize method of ISerializable is not implemented')

    def deserialize(self, *args, **Kwargs):
        '''
        Implements how item should be deserialized.

        Raises:
            NotImplementedError.
        '''
        raise NotImplementedError('deserialize method of ISerializable is not implemented')


class IItemBase(ISerializable):
    '''
    Item interface.

    Base for pins and nodes.
    '''

    def __init__(self):
        super(IItemBase, self).__init__()

    @property
    def uid(self):
        '''
        uid getter.

        used by graph and by nodes for fast members access
        pins inside node and nodes inside graph.

        Returns:
            universally unique identifier UUID class.
        '''
        pass

    @uid.setter
    def uid(self, value):
        '''
        uid setter.

        Args:
            value:  uuid4 universally unique identifier
        '''
        pass

    @uid.deleter
    def uid(self):
        '''
        uid deleter.

        uid is a fundamental element. Do not allow to accidentally delete it.

        Raises:
            NotImplementedError.
        '''
        raise NotImplementedError('uid property of IItemBase can not be deleted')

    def getName(self):
        '''
        returns item's name as string.

        Returns:
            string name of item.
        '''
        raise NotImplementedError('getName method of IItemBase is not implemented')

    def setName(self, name):
        '''
        sets item's name.

        Args:
            name: string to be used as name.
        '''
        raise NotImplementedError('setName method of IItemBase is not implemented')


class IPin(IItemBase):
    """
    Pin interface.
    """

    def __init__(self):
        super(IPin, self).__init__()

    @staticmethod
    def color():
        '''
        Defines what color pin will be drawn.

        Returns:
            QColor class.
        '''
        raise NotImplementedError('color method of IPin is not implemented')

    @staticmethod
    def pinDataTypeHint():
        """
        Static hint of what data type is this pin, as well as default value for this data type.

        Used to easily find pin classes by type id.


        Returns:
            A tuple containing data type id as first element + default value for this data type as second.

        Examples:
            # printing hints
            >>> somePin.pinDataTypeHint()
            (0, 0.0)
            >>> somePin.pinDataTypeHint()
            (3, False)

            # this is how it used in pins initialization
            >>> def _REGISTER_PIN_TYPE(pinSubclass):
            >>>     dType = pinSubclass.pinDataTypeHint()[0]
            >>>     if dType not in _PINS:
            >>>         _PINS[pinSubclass.pinDataTypeHint()[0]] = pinSubclass
            >>>     else:
            >>>         raise Exception("Error registering pin type {0}\n pin with ID [{1}] already registered".format(pinSubclass.__name__))

        @sa [DataTypes](@ref AGraphCommon.DataTypes)
        """
        raise NotImplementedError('pinDataTypeHint method of IPin is not implemented')

    def supportedDataTypes(self):
        '''
        An array of supported data types.

        Array of data types that can be casted to this type. For example - int can support float, or vector3 can support vector4 etc.
        '''
        raise NotImplementedError('supportedDataTypes method of IPin is not implemented')

    def defaultValue(self):
        '''
        Default value for this particular pin.

        This can be set whenever you need.

        @sa PyFlow.Pins
        '''
        raise NotImplementedError('defaultValue method of IPin is not implemented')

    def getData(self):
        raise NotImplementedError('getData method of IPin is not implemented')

    def setData(self, value):
        raise NotImplementedError('setData method of IPin is not implemented')

    def call(self):
        raise NotImplementedError('call method of IPin is not implemented')

    @property
    def dataType(self):
        raise NotImplementedError('dataType getter method of IPin is not implemented')

    @dataType.setter
    def dataType(self, value):
        raise NotImplementedError('dataType setter method of IPin is not implemented')

    def isUserStruct(self):
        raise NotImplementedError('isUserStruct method of IPin is not implemented')

    def getUserStruct(self):
        raise NotImplementedError('getUserStruct method of IPin is not implemented')

    def setUserStruct(self, inStruct):
        raise NotImplementedError('setUserStruct method of IPin is not implemented')


class INode(IItemBase):
    def __init__(self):
        super(INode, self).__init__()

    def compute(self):
        raise NotImplementedError('compute method of INode is not implemented')

    def isCallable(self):
        raise NotImplementedError('isCallable method of INode is not implemented')

    def addInputPin(self, pinName, dataType, foo=None):
        raise NotImplementedError('addInputPin method of INode is not implemented')

    def addOutputPin(self, pinName, dataType, foo=None):
        raise NotImplementedError('addOutputPin method of INode is not implemented')

    def getUniqPinName(self, name):
        raise NotImplementedError('getUniqPinName method of INode is not implemented')

    def postCreate(self, jsonTemplate=None):
        raise NotImplementedError('postCreate method of INode is not implemented')


## Base no gui Pin class
class PinBase(IPin):
    def __init__(self, name, owningNode, dataType, direction, userStructClass=None):
        super(PinBase, self).__init__()
        self._uid = uuid.uuid4()
        self._dataType = None
        self._userStructClass = userStructClass
        self._data = None
        self._defaultValue = None
        ## This flag for lazy evaluation
        # @sa @ref PinBase::getData
        self.dirty = True
        self._connected = False
        ## List of pins this pin connected to
        self.affects = []
        ## Lsit of pins connected to this pin
        self.affected_by = []
        ## List of connections
        self.edge_list = []

        ## Access to the node
        self.owningNode = weakref.ref(owningNode)
        self.setName(name)
        self.dataType = dataType

        ## Defines is this input pin or output
        self.direction = direction

    # ISerializable interface
    def serialize(self):
        data = {'name': self.name,
                'dataType': int(self.dataType),
                'direction': int(self.direction),
                'value': self.currentData(),
                'uuid': str(self.uid),
                'bDirty': self.dirty
                }
        return data

    @staticmethod
    def deserialize(owningNode, jsonData):
        pass

    # IItemBase interface

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self.owningNode().graph().pins[value] = self.owningNode().graph().pins.pop(self._uid)
        self._uid = value

    def setName(self, name):
        self.name = name.replace(" ", "_")

    def getName(self):
        return self.owningNode().name + '.' + self.name

    # IPin interface

    def color(self):
        return (125, 125, 200, 255)

    ## This used by node box to suggest nodes by type
    @staticmethod
    def pinDataTypeHint():
        return None

    def supportedDataTypes(self):
        return (self.dataType,)

    def defaultValue(self):
        return self._defaultValue

    ## retrieving the data
    def getData(self):
        # if not connected - compute and return
        if not self.hasConnections():
            if self.dataType == DataTypes.Array:
                return []
            if self.dirty:
                self.owningNode().compute()
                self.setClean()
            return self.currentData()

        if self.direction == PinDirection.Output:
            if self.dirty:
                self.owningNode().compute()
            self.setClean()
            return self._data
        if self.direction == PinDirection.Input:
            if self.dirty or self.owningNode().bCallable:
                out = [i for i in self.affected_by if i.direction == PinDirection.Output]
                if not out == []:
                    compute_order = self.owningNode().graph().getEvaluationOrder(out[0].parent())
                    # call from left to right
                    for layer in reversed(sorted([i for i in compute_order.keys()])):
                        for node in compute_order[layer]:
                            node.compute()
                    self.setClean()
                    return out[0]._data
            else:
                self.setClean()
                return self._data

    ## Setting the data
    def setData(self, data):
        self.setClean()
        self._data = data
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i._data = data
                i.setClean()

    ## Calling execution pin
    def call(self):
        pass

    ## Describes, what data type is this pin.
    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = value

    def isUserStruct(self):
        return self._userStructClass is not None

    def getUserStruct(self):
        return self._userStructClass

    def setUserStruct(self, inStruct):
        self._userStructClass = inStruct

    # PinBase methods

    def kill(self):
        if self.direction == PinDirection.Input and self.uid in self.owningNode().inputs:
            self.owningNode().inputs.pop(self.uid)
        if self.direction == PinDirection.Output and self.uid in self.owningNode().outputs:
            self.owningNode().outputs.pop(self.uid)
        if self.uid in self.owningNode().graph().pins:
            self.owningNode().graph().pins.pop(self.uid)

    def currentData(self):
        if self._data is None:
            return self._defaultValue
        return self._data

    def pinConnected(self, other):
        self._connected = True

    def pinDisconnected(self, other):
        if not self.hasConnections():
            self._connected = False

    def setClean(self):
        self.dirty = False
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i.dirty = False

    def hasConnections(self):
        if len(self.edge_list) == 0:
            return False
        else:
            return True

    def setDirty(self):
        if self.dataType == DataTypes.Exec:
            return
        self.dirty = True
        for i in self.affects:
            i.dirty = True

    def setDefaultValue(self, val):
        # In python, all user-defined classes are mutable
        # So make sure to store sepatrate copy of value
        # For example if this is a Matrix, default value will be changed each time data has been set in original Matrix
        self._defaultValue = deepcopy(val)


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
        for p in self.inputs.values() + self.outputs.values():
            if p.dataType == DataTypes.Exec:
                return True
        return False

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def addInputPin(self, pinName, dataType, defaultValue=None, foo=None):
        # check unique name
        pinName = self.getUniqPinName(pinName)
        p = PinBase(pinName, self, dataType, foo)
        self.inputs[p.uid] = p
        p.direction = PinDirection.Input
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        return p

    def addOutputPin(self, pinName, dataType, defaultValue=None, foo=None):
        p = PinBase(pinName, self, dataType, foo)
        self.outputs[p.uid] = p
        p.direction = PinDirection.Output
        if foo:
            p.call = foo
        if defaultValue is not None:
            p.setDefaultValue(defaultValue)
            p.setData(defaultValue)
        return p

    def getUniqPinName(self, name):
        pinNames = [i.name for i in self.inputs.values() + self.outputs.values()] + dir(self) + keyword.kwlist
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
            for p in self.inputs.values() + self.outputs.values():
                if p.name == name:
                    return p
        elif pinsSelectionGroup == PinSelectionGroup.Inputs:
            for p in self.inputs.values():
                if p.name == name:
                    return p
        else:
            for p in self.outputs.values():
                if p.name == name:
                    return p

    def postCreate(self, jsonTemplate=None):
        if self.isCallable():
            self.bCallable = True

    def computeCode(self):
        lines = inspect.getsourcelines(self.compute)[0]
        offset = lines[0].find("def compute")
        code = ""
        for line in lines:
            code += line[offset:]
        return code


class Graph(object):
    def __init__(self, name):
        super(Graph, self).__init__()
        self._debug = False
        self.name = name
        self.nodes = {}
        self.nodesPendingKill = []
        self.edges = {}
        self.pins = {}
        self.vars = {}

    def getUniqVarName(self, name):
        names = [v.name for v in self.vars.values()]
        if name not in names:
            return name
        idx = 0
        tmp = name
        while tmp in names:
            idx += 1
            tmp = name + str(idx)
        return name + str(idx)

    def getUniqNodeName(self, name):
        nodes_names = [n.name for n in self.nodes.values()]
        if name not in nodes_names:
            return name
        idx = 0
        tmp = name
        while tmp in nodes_names:
            idx += 1
            tmp = name + str(idx)
        return name + str(idx)

    def isDebug(self):
        return self._debug

    def setDebug(self, state):
        if not isinstance(state, bool):
            print 'bool expected. skipped'
            return
        self._debug = state

    def getEvaluationOrder(self, node):

        order = {0: []}

        # include first node only if it is callable
        if not node.bCallable:
            order[0].append(node)

        def foo(n, process=True):
            if not process:
                return
            next_layer_nodes = self.getNextLayerNodes(n, PinDirection.Input)

            layer_idx = max(order.iterkeys()) + 1
            for n in next_layer_nodes:
                if layer_idx not in order:
                    order[layer_idx] = []
                order[layer_idx].append(n)
            for i in next_layer_nodes:
                foo(i)
        foo(node)

        # make sure no copies of nodes in higher layers (non directional cycles)
        for i in reversed(sorted([i for i in order.iterkeys()])):
            for iD in range(i - 1, -1, -1):
                for check_node in order[i]:
                    if check_node in order[iD]:
                        order[iD].remove(check_node)
        return order

    @staticmethod
    def getNextLayerNodes(node, direction=PinDirection.Input):
        nodes = []
        '''
            callable nodes skipped
            because execution flow is defined by execution wires
        '''
        if direction == PinDirection.Input:
            if not len(node.inputs) == 0:
                for i in node.inputs.values():
                    if not len(i.affected_by) == 0:
                        for a in i.affected_by:
                            if not a.parent().bCallable:
                                nodes.append(a.parent())
            return nodes
        if direction == PinDirection.Output:
            if not len(node.outputs) == 0:
                for i in node.outputs.values():
                    if not len(i.affects) == 0:
                        for p in i.affects:
                            if not p.parent().bCallable:
                                nodes.append(p.parent())
            return nodes

    def getNodes(self):
        return self.nodes.values()

    def getNodeByName(self, name):
        for i in self.nodes.values():
            if i.name == name:
                return i
        return None

    def addNode(self, node, jsonTemplate=None):
        if not node:
            return False
        if node.uid in self.nodes:
            return False
        self.nodes[node.uid] = node
        if jsonTemplate is not None:
            node.setPosition(jsonTemplate['x'], jsonTemplate['y'])
        else:
            node.setPosition(0, 0)
        # add pins
        for i in node.inputs.values():
            self.pins[i.uid] = i
        for o in node.outputs.values():
            self.pins[o.uid] = o
        return True

    def removeNode(self, node):
        uid = node.uid
        node.kill()
        self.nodes.pop(uid)

    def count(self):
        return self.nodes.__len__()

    def canConnectPins(self, src, dst):
        debug = self.isDebug()
        if src.direction == PinDirection.Input:
            src, dst = dst, src

        if src.uid not in self.pins:
            print('scr not in graph.pins')
            return False
        if dst.uid not in self.pins:
            print('dst not in graph.pins')
            return False

        if src.dataType not in dst.supportedDataTypes():
            print("[{0}] is not conmpatible with [{1}]".format(getDataTypeName(src.dataType), getDataTypeName(dst.dataType)))
            return False
        else:
            if src.dataType is DataTypes.Exec:
                if dst.dataType is not DataTypes.Exec:
                    print("[{0}] is not conmpatible with [{1}]".format(getDataTypeName(src.dataType), getDataTypeName(dst.dataType)))
                    return False

        if src in dst.affected_by:
            if debug:
                print('already connected. skipped')
            return False
        if src.direction == dst.direction:
            if debug:
                print('same types can not be connected')
            return False
        if src.owningNode == dst.owningNode:
            if debug:
                print('can not connect to self')
            return False
        if cycle_check(src, dst):
            if debug:
                print('cycles are not allowed')
            return False
        return True

    def addEdge(self, src, dst):
        if not self.canConnectPins(src, dst):
            return False

        if src.direction == PinDirection.Input:
            src, dst = dst, src

        # input value pins can have one output connection
        # output value pins can have any number of connections
        if not src.dataType == DataTypes.Exec and dst.hasConnections():
            dst.disconnectAll()
        # input execs can have any number of connections
        # output execs can have only one connection
        if src.dataType == DataTypes.Exec and dst.dataType == DataTypes.Exec and src.hasConnections():
            src.disconnectAll()

        pinAffects(src, dst)
        src.setDirty()
        dst._data = src._data
        dst.pinConnected(src)
        src.pinConnected(dst)
        push(dst)
        return True

    def removeEdge(self, edge):
        edge.source().affects.remove(edge.destination())
        edge.source().edge_list.remove(edge)
        edge.destination().affected_by.remove(edge.source())
        edge.destination().edge_list.remove(edge)
        edge.destination().pinDisconnected(edge.source())
        edge.source().pinDisconnected(edge.destination())
        push(edge.destination())

    def plot(self):
        print self.name + '\n----------\n'
        for n in self.getNodes():
            print(n.name)
            for inp in n.inputs.values():
                print '|---', inp._rawPin.name, 'data - {0}'.format(inp._rawPin.currentData()), \
                    'affects on', [i._rawPin.name for i in inp._rawPin.affects], \
                    'affected_by ', [p._rawPin.name for p in inp._rawPin.affected_by], \
                    'DIRTY ', inp._rawPin.dirty
                for e in inp._rawPin.edge_list:
                    print '\t|---', e.__str__()
            for out in n.outputs.values():
                print '|---' + out._rawPin.name, 'data - {0}'.format(out._rawPin.currentData()), \
                    'affects on', [i._rawPin.name for i in out._rawPin.affects], \
                    'affected_by ', [p._rawPin.name for p in out._rawPin.affected_by], \
                    'DIRTY', out._rawPin.dirty
                for e in out._rawPin.edge_list:
                    print '\t|---', e.__str__()

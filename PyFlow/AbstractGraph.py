from AGraphCommon import *
import weakref
import uuid
import inspect
import keyword
from collections import OrderedDict
import itertools
from copy import deepcopy


class ISerializable(object):
    """docstring for ISerializable"""
    def __init__(self):
        super(ISerializable, self).__init__()

    def serialize(self):
        raise NotImplementedError('serialize method of ISerializable is not implemented')

    def deserialize(self):
        raise NotImplementedError('deserialize method of ISerializable is not implemented')


class IItemBase(object):

    def __init__(self):
        super(IItemBase, self).__init__()
        self._uid = uuid.uuid4()

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @uid.deleter
    def uid(self):
        raise NotImplementedError('uid property of IItemBase can not be deleted')

    def getName(self):
        raise NotImplementedError('getName method of IItemBase is not implemented')

    def setName(self):
        raise NotImplementedError('setName method of IItemBase is not implemented')


class IPin(IItemBase, ISerializable):
    """Pin interface"""

    def __init__(self):
        super(IPin, self).__init__()

    @staticmethod
    def color():
        raise NotImplementedError('color method of IPin is not implemented')

    def supportedDataTypes(self):
        raise NotImplementedError('supportedDataTypes method of IPin is not implemented')

    def defaultValue(self):
        raise NotImplementedError('defaultValue method of IPin is not implemented')

    def setData(self, value):
        raise NotImplementedError('setData method of IPin is not implemented')


class INode(IItemBase, ISerializable):
    def __init__(self):
        super(INode, self).__init__()

    def compute(self):
        raise NotImplementedError('compute method of INode is not implemented')


class PinBase(IPin, ISerializable):
    def __init__(self, name, parent, dataType, direction):
        super(PinBase, self).__init__()
        self.parent = weakref.ref(parent)
        self.setName(name)
        self._dataType = None
        self._data = None
        self._defaultValue = None
        self.dataType = dataType

        self.affects = []
        self.affected_by = []
        self.edge_list = []
        self.direction = direction
        self.dirty = True
        self._connected = False

    def setName(self, name):
        self.name = name.replace(" ", "_")

    @IItemBase.uid.setter
    def uid(self, value):
        self.parent().graph().pins[value] = self.parent().graph().pins.pop(self._uid)
        self._uid = value

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = value

    def supportedDataTypes(self):
        return (self.dataType,)

    def kill(self):
        if self.direction == PinDirection.Input and self.uid in self.parent().inputs:
            self.parent().inputs.pop(self.uid)
        if self.direction == PinDirection.Output and self.uid in self.parent().outputs:
            self.parent().outputs.pop(self.uid)
        if self.uid in self.parent().graph().pins:
            self.parent().graph().pins.pop(self.uid)

    def getName(self):
        return self.parent().name + '.' + self.name

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

    def getData(self):
        # if not connected - return data
        if not self.hasConnections():
            if self.dataType == DataTypes.Array:
                return []
            return self.currentData()

        if self.direction == PinDirection.Output:
            if self.dirty:
                self.parent().compute()
            self.setClean()
            return self._data
        if self.direction == PinDirection.Input:
            if self.dirty or self.parent().bCallable:
                out = [i for i in self.affected_by if i.direction == PinDirection.Output]
                if not out == []:
                    compute_order = self.parent().graph().getEvaluationOrder(out[0].parent())
                    # call from left to right
                    for layer in reversed(sorted([i for i in compute_order.keys()])):
                        for node in compute_order[layer]:
                            node.compute()
                    self.setClean()
                    return out[0]._data
            else:
                self.setClean()
                return self._data

    def call(self):
        pass

    def defaultValue(self):
        return self._defaultValue

    def setDefaultValue(self, val):
        # In python, all user-defined classes are mutable
        # So make sure to store sepatrate copy of value
        # For example if this is a Matrix, default value will be changed each time data has been set in original Matrix
        self._defaultValue = deepcopy(val)

    def setData(self, data):
        self.setClean()
        if self.direction == PinDirection.Output:
            for i in self.affects:
                i._data = data
                i.setClean()


class NodeBase(INode):
    def __init__(self, name, graph):
        super(NodeBase, self).__init__()
        self.graph = weakref.ref(graph)
        self.name = name
        self.inputs = OrderedDict()
        self.outputs = OrderedDict()
        self.x = 0.0
        self.y = 0.0
        self.bCallable = False

    # ###################
    # IItemBase interface begin
    # ###################

    @IItemBase.uid.setter
    def uid(self, value):
        if self._uid in self.graph().nodes:
            self.graph().nodes[value] = self.graph().nodes.pop(self._uid)
            self._uid = value

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    # ###################
    # IItemBase interface end
    # ###################

    # ###############
    # INode interface begin
    # ###############
    def compute(self):
        '''
        node calculations here
        '''
        # getting data from inputs

        # do stuff

        # write data to outputs
        return

    # ###############
    # INode interface end
    # ###############

    def isCallable(self):
        for p in self.inputs.values() + self.outputs.values():
            if p.dataType == DataTypes.Exec:
                return True
        return False

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def addInputPin(self, pinName, dataType, foo=None):
        p = PinBase(pinName, self, dataType, foo)
        self.inputs[p.uid] = p
        p.direction = PinDirection.Input
        if foo:
            p.call = foo
        return p

    def addOutputPin(self, pinName, dataType, foo=None):
        p = PinBase(pinName, self, dataType, foo)
        self.outputs[p.uid] = p
        p.direction = PinDirection.Output
        if foo:
            p.call = foo
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

    def addNode(self, node, jsonTemplate):
        if not node:
            return False
        if node.uid in self.nodes:
            return False
        self.nodes[node.uid] = node
        node.setPosition(jsonTemplate['x'], jsonTemplate['y'])
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
        if src.parent == dst.parent:
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
            print n.name
            for inp in n.inputs.values():
                print '|---', inp.name, 'data - {0}'.format(inp.currentData()), \
                    'affects on', [i.name for i in inp.affects], \
                    'affected_by ', [p.name for p in inp.affected_by], \
                    'DIRTY ', inp.dirty
                for e in inp.edge_list:
                    print '\t|---', e.__str__()
            for out in n.outputs.values():
                print '|---' + out.name, 'data - {0}'.format(out.currentData()), \
                    'affects on', [i.name for i in out.affects], \
                    'affected_by ', [p.name for p in out.affected_by], \
                    'DIRTY', out.dirty
                for e in out.edge_list:
                    print '\t|---', e.__str__()

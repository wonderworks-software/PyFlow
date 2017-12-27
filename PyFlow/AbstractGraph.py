from threading import Thread
from AGraphCommon import *
import weakref
import uuid
import inspect
import keyword


class PinBase(object):
    def __init__(self, name, parent, dataType):
        super(PinBase, self).__init__()
        self._uid = uuid.uuid4()
        self.name = name.replace(" ", "_")
        self.parent = weakref.ref(parent)
        self.object_type = ObjectTypes.Pin
        self._dataType = None
        self.supportedDataTypes = []
        self.dataType = dataType

        self.affects = []
        self.affected_by = []
        self.edge_list = []
        self.type = None
        self.dirty = True
        self._connected = False
        # set default values
        self._data = getDefaultDataValue(self._dataType)
        # put self in graph
        self.parent().graph().pins[self.uid] = self

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self.parent().graph().pins.pop(self._uid)
        self._uid = value
        self.parent().graph().pins[self._uid] = self

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = value

        self.supportedDataTypes = list(set([value]))
        if self.dataType == DataTypes.Exec or self.dataType == DataTypes.Any:
            self.supportedDataTypes.append(value)

    def kill(self):
        self.parent().graph().pins.pop(self.uid)
        if self.type == PinTypes.Input and self.uid in self.parent().inputs:
            self.parent().inputs.pop(self.uid)
        if self.type == PinTypes.Output and self.uid in self.parent().outputs:
            self.parent().outputs.pop(self.uid)

    def pinName(self):
        return self.parent().name + '.' + self.name

    def currentData(self):
        if self._data is None:
            return getDefaultDataValue(self._dataType)
        return self._data

    def pinConnected(self, other):
        self._connected = True

    def pinDisconnected(self, other):
        if not self.hasConnections():
            self._connected = False

    def setClean(self):
        self.dirty = False

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
            return self.currentData()

        if self.type == PinTypes.Output:
            if self.dirty:
                compute_order = self.parent().graph().getEvaluationOrder(self.parent())
                for i in reversed(sorted([i for i in compute_order.keys()])):
                    if not self.parent().graph().isMultithreaded():
                        for n in compute_order[i]:
                            n.compute()
                    else:
                        calc_multithreaded(compute_order[i])
                return self._data
            else:
                return self._data
        if self.type == PinTypes.Input:
            if self.dirty:
                out = [i for i in self.affected_by if i.type == PinTypes.Output]
                if not out == []:
                    compute_order = out[0].parent().graph().getEvaluationOrder(out[0].parent())
                    for i in reversed(sorted([i for i in compute_order.keys()])):
                        if not self.parent().graph().isMultithreaded():
                            for n in compute_order[i]:
                                n.compute()
                        else:
                            calc_multithreaded(compute_order[i])
                    return out[0]._data
            else:
                return self._data
        else:
            return self._data

    @staticmethod
    def str2bool(v):
        return v.lower() in ("true", "1")

    def call(self):
        for p in self.affects:
            p.call()

    def setData(self, data):
        if self._dataType == DataTypes.Float:
            try:
                self._data = float(data)
            except:
                self._data = getDefaultDataValue(self._dataType)
        if self._dataType == DataTypes.Int:
            try:
                self._data = int(data)
            except:
                self._data = getDefaultDataValue(self._dataType)
        if self._dataType == DataTypes.String:
            self._data = str(data)
        if self._dataType == DataTypes.Array:
            self._data = data
        if self._dataType == DataTypes.Bool:
            self._data = bool(data)
        if self._dataType == DataTypes.Any:
            self._data = data

        self.setClean()
        if self.type == PinTypes.Output:
            for i in self.affects:
                i._data = data
                i.setClean()


class NodeBase(object):
    def __init__(self, name, graph):
        super(NodeBase, self).__init__()
        self._uid = uuid.uuid4()
        self.graph = weakref.ref(graph)
        self.name = name
        self.object_type = ObjectTypes.Node
        self.inputs = {}
        self.outputs = {}
        self.x = 0.0
        self.y = 0.0

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self.graph().nodes.pop(self._uid)
        self._uid = value
        self.graph().nodes[self._uid] = self

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def addInputPin(self, pinName, dataType, foo=None):
        p = PinBase(pinName, self, dataType, foo)
        self.inputs[p.uid] = p
        p.type = PinTypes.Input
        if foo:
            p.call = foo
        return p

    def addOutputPin(self, pinName, dataType, foo=None):
        p = PinBase(pinName, self, dataType, foo)
        self.outputs[p.uid] = p
        p.type = PinTypes.Output
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
        pass

    def computeCode(self):
        lines = inspect.getsourcelines(self.compute)[0]
        offset = lines[0].find("def compute")
        code = ""
        for line in lines:
            code += line[offset:]
        return code

    def compute(self):
        '''
        node calculations here
        '''
        # getting data from inputs

        # do stuff

        # write data to outputs
        return


class Graph(object):
    def __init__(self, name):
        super(Graph, self).__init__()
        self.object_type = ObjectTypes.Graph
        self._debug = False
        self._multithreaded = False
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

    def isMultithreaded(self):
        return self._multithreaded

    def setMultithreaded(self, state):
        if not isinstance(state, bool):
            print 'bool expected. skipped'
            return
        self._multithreaded = state

    def getEvaluationOrder(self, node, dirty_only=True):

        order = {0: [node]}

        def foo(n):
            next_layer_nodes = self.getNextLayerNodes(n, PinTypes.Input, dirty_only)
            layer_idx = max(order.iterkeys()) + 1
            for n in next_layer_nodes:
                if layer_idx not in order:
                    order[layer_idx] = []
                order[layer_idx].append(n)
            if not next_layer_nodes == []:
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
    def getNextLayerNodes(node, direction=PinTypes.Input, dirty_only=False):
        nodes = []
        if direction == PinTypes.Input:
            if not node.inputs.values() == []:
                for i in node.inputs.values():
                    if not i.affected_by == []:
                        for a in i.affected_by:
                            if not dirty_only:
                                nodes.append(a.parent())
                            else:
                                if a.dirty:
                                    nodes.append(a.parent())
            return nodes
        if direction == PinTypes.Output:
            if not node.outputs.values() == []:
                for i in node.outputs.values():
                    if not i.affects == []:
                        for p in i.affects:
                            if not dirty_only:
                                nodes.append(p.parent())
                            else:
                                if not [dout for dout in p.affects if dout.dirty] == []:
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
        node.postCreate(jsonTemplate)
        return True

    def removeNode(self, node):
        uid = node.uid
        node.kill()
        self.nodes.pop(uid)

    def count(self):
        return self.nodes.__len__()

    def addEdge(self, src, dst):
        debug = self.isDebug()
        if src.type == PinTypes.Input:
            src, dst = dst, src

        if DataTypes.Any not in dst.supportedDataTypes:
            if src.dataType not in dst.supportedDataTypes:
                print("data types error", src.dataType, dst.dataType)
                return False
        else:
            if src.dataType == DataTypes.Exec:
                if dst.dataType not in [DataTypes.Exec]:
                    print("data types error", src.dataType, dst.dataType)
                    return False

        if src in dst.affected_by:
            if debug:
                print('already connected. skipped')
            return False
        if src.type == dst.type:
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

        # input data ports can have one output connection
        # output data ports can have any number of connections
        if not src.dataType == DataTypes.Exec and dst.hasConnections():
            dst.disconnectAll()
        # input execs can have any number of connections
        # output execs can have only one connection
        if src.dataType == DataTypes.Exec and dst.dataType == DataTypes.Exec and src.hasConnections():
            src.disconnectAll()

        portAffects(src, dst)
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

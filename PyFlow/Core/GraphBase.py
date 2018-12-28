from PyFlow.Core.AGraphCommon import *


class GraphBase(object):
    def __init__(self, name):
        super(GraphBase, self).__init__()
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

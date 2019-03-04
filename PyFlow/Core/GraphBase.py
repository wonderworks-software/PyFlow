from PyFlow.Core.AGraphCommon import *
from PyFlow import CreateRawPin 
import weakref


class GraphBase(object):
    def __init__(self, name):
        super(GraphBase, self).__init__()
        self._debug = False
        self.name = name
        self.nodes = {}
        self.edges = {}
        self.pins = {}
        self.vars = {}

    def getVars(self):
        return self.vars.values()

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
            print('bool expected. skipped')
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

            layer_idx = max(order.keys()) + 1
            for n in next_layer_nodes:
                if layer_idx not in order:
                    order[layer_idx] = []
                order[layer_idx].append(n)
            for i in next_layer_nodes:
                foo(i)
        foo(node)

        # make sure no copies of nodes in higher layers (non directional cycles)
        for i in reversed(sorted([i for i in order.keys()])):
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
                            if not a.owningNode().bCallable:
                                nodes.append(a.owningNode())
            return nodes
        if direction == PinDirection.Output:
            if not len(node.outputs) == 0:
                for i in node.outputs.values():
                    if not len(i.affects) == 0:
                        for p in i.affects:
                            if not p.owningNode().bCallable:
                                nodes.append(p.owningNode())
            return nodes

    def getNodes(self):
        return self.nodes.values()

    def getNodeByName(self, name):
        for i in self.nodes.values():
            if i.name == name:
                return i
        return None

    def findPin(self, uid):
        return self.findPinByUID(uid)

    def findPinByUID(self, uid):
        uiPin = None
        if uid in self.pins:
            uiPin = self.pins[uid]
        return uiPin

    def findPinByName(self, pinName):
        uiPin = None
        for pin in self.pins.values():
            if pinName == pin.getName():
                uiPin = pin
                break
        return uiPin

    def addNode(self, node):
        assert(node is not None), "failed to add node, None is passed"
        if node.uid in self.nodes:
            return False
        self.nodes[node.uid] = node
        node.graph = weakref.ref(self)

        # add pins
        for i in node.inputs.values():
            self.pins[i.uid] = i
        for o in node.outputs.values():
            self.pins[o.uid] = o
        node.setName(self.getUniqNodeName(node.name))
        return True

    def removeNode(self, node):
        uid = node.uid
        node.kill()
        self.nodes.pop(uid)

    def count(self):
        return self.nodes.__len__()

    def canConnectPins(self, src, dst):
        debug = self.isDebug()
        if src is None or dst is None:
            print("can not connect pins")
            return False
        if src.direction == PinDirection.Input:
            src, dst = dst, src

        if src.uid not in self.pins:
            print('scr ({}) not in graph.pins'.format(src.getName()))
            return False
        if dst.uid not in self.pins:
            print('dst ({}) not in graph.pins'.format(dst.getName()))
            return False

        if src.dataType == "AnyPin" and not cycle_check(src, dst) and not src.direction == dst.direction:
            return True

        if src.dataType not in dst.supportedDataTypes() and not src.dataType == "AnyPin":
            print("[{0}] is not conmpatible with [{1}]".format(src.dataType, dst.dataType))
            return False
        else:
            if src.dataType is 'ExecPin':
                if dst.dataType is not 'ExecPin' and dst.dataType is not "AnyPin":
                    print("[{0}] is not conmpatible with [{1}]".format(src.dataType, dst.dataType))
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

        if dst.constraint != None:
            if dst.dataType != "AnyPin":
                cheked = []
                if dst.isAny:
                    free = dst.checkFree([],False)
                    if not free:
                        a = CreateRawPin("", None, dst.dataType, 0)
                        if src.dataType not in a.supportedDataTypes():
                            print("[{0}] is not conmpatible with [{1}]".format(getDataTypeName(src.dataType), getDataTypeName(dst.dataType)))
                            return False
                        del a                
        return True

    def addEdge(self, src, dst):
        if not self.canConnectPins(src, dst):
            return False

        if src.direction == PinDirection.Input:
            src, dst = dst, src

        # input value pins can have one output connection
        # output value pins can have any number of connections
        if not src.dataType == 'ExecPin' and dst.hasConnections():
            dst.disconnectAll()
        # input execs can have any number of connections
        # output execs can have only one connection
        if src.dataType == 'ExecPin' and dst.dataType == 'ExecPin' and src.hasConnections():
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
        print(self.name + '\n----------\n')
        for n in self.getNodes():
            print("Node:", n.name)
            for inp in n.inputs.values():
                print(inp.getName(), 'data - {0}'.format(inp.currentData()),
                      'affects on', [i.getName() for i in inp.affects],
                      'affected_by ', [p.getName() for p in inp.affected_by],
                      'DIRTY ', inp.dirty)
            for out in n.outputs.values():
                print(out.getName(), 'data - {0}'.format(out.currentData()),
                      'affects on', [i.getName() for i in out.affects],
                      'affected_by ', [p.getName() for p in out.affected_by],
                      'DIRTY', out.dirty)

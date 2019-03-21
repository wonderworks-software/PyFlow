import weakref

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Variable import Variable


class GraphBase(object):
    def __init__(self, name, parentGraph=None):
        super(GraphBase, self).__init__()
        self._parentGraph = parentGraph
        self.name = name
        self.nodes = {}
        self.connections = {}
        self.vars = {}

    @property
    def parentGraph(self):
        return self._parentGraph

    @property
    def pins(self):
        result = {}
        for n in self.getNodes():
            for pin in tuple(n.inputs.values()) + tuple(n.outputs.values()):
                result[pin.uid] = pin
        return result

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None):
        var = Variable(getPinDefaultValueByType(dataType), self.getUniqVarName('var'), dataType, accessLevel=accessLevel, uid=uid)
        self.vars[var.uid] = var
        return var

    def killVariable(self, var):
        assert(isinstance(var, Variable))
        if var.uid in self.vars:
            popped = self.vars.pop(var.uid)
            popped.killed.send()

    def isRoot(self):
        return self._parentGraph is None

    def getVars(self):
        """Returns this graph variables as well as all parent graph's ones

        returns:
            {'graphName': varsDict, ...}
        """
        result = dict()
        result[self.name] = self.vars
        parent = self.parentGraph
        while parent is not None:
            # TODO: check for unique graph names
            result[parent.name] = parent.vars
            parent = parent.parent
        return result

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
            nodeInputs = node.inputs
            if not len(nodeInputs) == 0:
                for i in nodeInputs.values():
                    if not len(i.affected_by) == 0:
                        for a in i.affected_by:
                            if not a.owningNode().bCallable:
                                nodes.append(a.owningNode())
            return nodes
        if direction == PinDirection.Output:
            nodeOutputs = node.outputs
            if not len(nodeOutputs) == 0:
                for i in nodeOutputs.values():
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

    def getNodesByClassName(self, className):
        nodes = []
        for i in self.nodes.values():
            if i.__class__.__name__ == className:
                nodes.append(i)
        return nodes

    def findPinByUID(self, uid):
        pin = None
        if uid in self.pins:
            pin = self.pins[uid]
        return pin

    def findPinByName(self, pinName):
        pin = None
        for pin in self.pins.values():
            if pinName == pin.getName():
                pin = pin
                break
        return pin

    def addNode(self, node, jsonTemplate=None):
        assert(node is not None), "failed to add node, None is passed"
        if node.uid in self.nodes:
            return False
        self.nodes[node.uid] = node
        node.graph = weakref.ref(self)
        node.setName(self.getUniqNodeName(node.name))
        node.postCreate(jsonTemplate)
        return True

    def count(self):
        return self.nodes.__len__()

    def canConnectPins(self, src, dst):

        if src is None or dst is None:
            print("can not connect pins")
            if src is None:
                print("src is None")
            if dst is None:
                print("dst is None")
            return False

        if src.direction == PinDirection.Input:
            src, dst = dst, src

        if src.direction == dst.direction:
            return False

        if cycle_check(src, dst):
            print('cycles are not allowed')
            return False

        allPins = self.pins
        if src.uid not in allPins:
            print('scr ({}) not in graph.pins'.format(src.getName()))
            return False
        if dst.uid not in allPins:
            print('dst ({}) not in graph.pins'.format(dst.getName()))
            return False

        if src.dataType == "AnyPin" and not cycle_check(src, dst):
            return True

        if dst.dataType == "AnyPin":
            if src.dataType not in findPinClassByType(dst.activeDataType).supportedDataTypes():
                return False

        if src.dataType not in dst.supportedDataTypes() and not src.dataType == "AnyPin":
            print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
            return False
        else:
            if src.dataType is 'ExecPin':
                if dst.dataType != 'ExecPin' and dst.dataType != 'AnyPin':
                    print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
                    return False

        if src in dst.affected_by:
            print('already connected. skipped')
            return False
        if src.direction == dst.direction:
            print('same side pins can not be connected')
            return False
        if src.owningNode == dst.owningNode:
            print('can not connect to owning node')
            return False

        if dst.constraint is not None:
            if dst.dataType != "AnyPin":
                if dst.isAny:
                    free = dst.checkFree([], False)
                    if not free:
                        pinClass = findPinClassByType(dst.dataType)
                        if src.dataType not in pinClass.supportedDataTypes():
                            print("[{0}] is not compatible with [{1}]".format(src.dataType, dst.dataType))
                            return False
        return True

    def connectPins(self, src, dst):
        if not self.canConnectPins(src, dst):
            return False

        if src.direction == PinDirection.Input:
            src, dst = dst, src

        # input value pins can have one output connection
        # output value pins can have any number of connections
        if src.dataType not in ['ExecPin', 'AnyPin'] and dst.hasConnections():
            dst.disconnectAll()
        if src.dataType == 'AnyPin' and dst.dataType != 'ExecPin' and dst.hasConnections():
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

    def plot(self):
        print(self.name + '\n----------\n')
        for n in self.getNodes():
            print("Node:", n.name, n.uid)
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

import weakref

from PyFlow.Core.Common import *
from PyFlow import CreateRawPin
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Variable import Variable
from PyFlow.Core.GraphTree import GraphTree


class GraphBase(object):
    def __init__(self, name):
        super(GraphBase, self).__init__()
        self.__name = name
        self.nodes = {}
        self.connections = {}
        self.vars = {}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        assert(isinstance(value, str))
        self.__name = value

    def Tick(self, deltaTime):
        for node in self.nodes.values():
            node.Tick(deltaTime)

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
        node.setName(GraphTree().getUniqNodeName(node.name))
        node.postCreate(jsonTemplate)
        return True

    def count(self):
        return self.nodes.__len__()

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

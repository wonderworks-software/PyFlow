import weakref
from blinker import Signal
from treelib import Tree
from multipledispatch import dispatch

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow import CreateRawPin
from PyFlow import getRawNodeInstance
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Variable import Variable
from PyFlow.Core.Interfaces import ISerializable


class GraphBase(ISerializable):
    def __init__(self, name, manager, category='', *args, **kwargs):
        super(GraphBase, self).__init__(*args, **kwargs)
        self.graphManager = manager
        # signals
        self.inputPinCreated = Signal(object)
        self.outputPinCreated = Signal(object)
        self.nameChanged = Signal(str)
        self.categoryChanged = Signal(str)

        self.parentGraph = manager.activeGraph() if manager.activeGraph() is not None else None

        self.__name = name
        self.__category = category
        self.nodes = {}
        self.vars = {}

        manager.add(self)

    def depth(self):
        result = 1
        parent = self.parentGraph
        while parent is not None:
            result += 1
            parent = parent.parentGraph
        return result

    def getVarList(self):
        """return list of variables from active graph
        """
        result = list(self.vars.values())
        parent = self.parentGraph
        while parent is not None:
            result += list(parent.vars.values())
            parent = parent.parentGraph
        return result

    def serialize(self, *args, **Kwargs):
        result = {
            'name': self.name,
            'category': self.category,
            'vars': [v.serialize() for v in self.vars.values()],
            'nodes': [n.serialize() for n in self.nodes.values()],
            'depth': self.depth()
        }
        return result

    @staticmethod
    def deserialize(jsonData, manager, *args, **kwargs):
        # create graph
        graph = GraphBase(jsonData['name'], manager, jsonData['category'])
        # restore vars
        for varJson in jsonData['vars']:
            var = Variable.deserialize(varJson, *args, **kwargs)
            graph.vars[var.uid] = var
        # restore nodes
        for nodeJson in jsonData['nodes']:
            # check if variable getter or setter and pass variable
            nodeArgs = args
            nodeKwargs = kwargs
            if nodeJson['type'] in ('getVar', 'setVar'):
                kwargs['var'] = graph.vars[uuid.UUID(nodeJson['varUid'])]
            node = NodeBase.deserialize(nodeJson, *nodeArgs, **nodeKwargs)
            # set pin uids
            graph.addNode(node, nodeJson)

        # restore connections
        graphPins = graph.pins
        for nodeJson in jsonData['nodes']:
            for nodeOutputJson in nodeJson['outputs']:
                lhsPin = graphPins[uuid.UUID(nodeOutputJson['uuid'])]
                for rhsUidStr in nodeOutputJson['linkedTo']:
                    rhsPin = graphPins[uuid.UUID(rhsUidStr)]
                    connected = connectPins(lhsPin, rhsPin)
                    assert(connected is True), "Failed to restore connection"
        return graph

    def clear(self):
        for node in list(self.nodes.values()):
            node.kill()
        self.nodes.clear()

        for var in list(self.vars.values()):
            # TODO: remove variable
            pass
        self.vars.clear()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        assert(isinstance(value, str))
        # TODO: remove this. graph manager should store graphs by uuids
        # actualize internal graphManager data
        self.graphManager._graphs[value] = self.graphManager._graphs.pop(self.__name)

        self.__name = value
        self.nameChanged.send(self.__name)

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        assert(isinstance(value, str))
        self.__category = value
        self.categoryChanged.send(self.__category)

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

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None, name="var"):
        name = self.graphManager.getUniqVariableName(name)
        var = Variable(self, getPinDefaultValueByType(dataType), name, dataType, accessLevel=accessLevel, uid=uid)
        self.vars[var.uid] = var
        return var

    def killVariable(self, var):
        assert(isinstance(var, Variable))
        if var.uid in self.vars:
            popped = self.vars.pop(var.uid)
            popped.killed.send()

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
        """return all nodes without compound's nodes
        """
        return [n for n in self.nodes.values()]

    @dispatch(str)
    def findNode(self, name):
        for i in self.nodes.values():
            if i.name == name:
                return i
        return None

    def getNodesByClassName(self, className):
        nodes = []
        for i in self.getNodes():
            if i.__class__.__name__ == className:
                nodes.append(i)
        return nodes

    @dispatch(uuid.UUID)
    def findPin(self, uid):
        pin = None
        if uid in self.pins:
            pin = self.pins[uid]
        return pin

    @dispatch(str)
    def findPin(self, pinName):
        pin = None
        for pin in self.pins.values():
            if pinName == pin.getName():
                pin = pin
                break
        return pin

    def getInputNode(self):
        """Creates and adds to graph 'graphInputs' node

        pins on this node will be exposed on compound node as input pins
        """
        node = getRawNodeInstance("graphInputs", "PyflowBase")
        self.addNode(node)
        return node

    def getOutputNode(self):
        """Creates and adds to graph 'graphOutputs' node.

        pins on this node will be exposed on compound node as output pins
        """
        node = getRawNodeInstance("graphOutputs", "PyflowBase")
        self.addNode(node)
        return node

    def addNode(self, node, jsonTemplate=None):
        assert(node is not None), "failed to add node, None is passed"
        if node.uid in self.nodes:
            return False
        self.nodes[node.uid] = node
        node.graph = weakref.ref(self)
        node.setName(self.graphManager.getUniqNodeName(node.name))
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

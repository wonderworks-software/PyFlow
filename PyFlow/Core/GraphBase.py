import weakref
from blinker import Signal
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
    def __init__(self, name, manager, parentGraph=None, category='', uid=None, *args, **kwargs):
        super(GraphBase, self).__init__(*args, **kwargs)
        self.graphManager = manager
        self._isRoot = False
        # signals
        self.nameChanged = Signal(str)
        self.categoryChanged = Signal(str)

        self.__name = name
        self.__category = category

        self._parentGraph = None
        self.childGraphs = set()

        self.parentGraph = parentGraph

        self.nodes = {}
        self.vars = {}
        self.uid = uuid.uuid4() if uid is None else uid

        manager.add(self)

    def setIsRoot(self, bIsRoot):
        self._isRoot = bIsRoot

    def isRoot(self):
        return self._isRoot

    @property
    def parentGraph(self):
        return self._parentGraph

    @parentGraph.setter
    def parentGraph(self, newParentGraph):
        if self.isRoot():
            self._parentGraph = None
            return

        if newParentGraph is not None:
            if self._parentGraph is not None:
                # remove self from old parent's children set
                if self in self._parentGraph.childGraphs:
                    self._parentGraph.childGraphs.remove(self)
            # add self to new parent's children set
            newParentGraph.childGraphs.add(self)
            # update parent
            self._parentGraph = newParentGraph

    def depth(self):
        result = 1
        parent = self._parentGraph
        while parent is not None:
            result += 1
            parent = parent.parentGraph
        return result

    def getVarList(self):
        """return list of variables from active graph
        """
        result = list(self.vars.values())
        parent = self._parentGraph
        while parent is not None:
            result += list(parent.vars.values())
            parent = parent.parentGraph
        return result

    def serialize(self, copying=False, *args, **Kwargs):
        result = {
            'name': self.name,
            'category': self.category,
            'vars': [v.serialize(copying=copying) for v in self.vars.values()],
            'nodes': [n.serialize(copying=copying) for n in self.nodes.values()],
            'depth': self.depth(),
            'isRoot': self.isRoot(),
            'parentGraphName': str(self._parentGraph.name) if self._parentGraph is not None else str(None)
        }
        return result

    def populateFromJson(self, jsonData):
        self.clear()
        parentGraphName = jsonData['parentGraphName']
        parentGraph = self.graphManager.findGraph(parentGraphName)
        self.parentGraph = parentGraph
        self.name = jsonData['name']
        self.category = jsonData['category']
        self.setIsRoot(jsonData['isRoot'])
        # restore vars
        for varJson in jsonData['vars']:
            var = Variable.deserialize(self, varJson)
            self.vars[var.uid] = var
        # restore nodes
        for nodeJson in jsonData['nodes']:
            # check if variable getter or setter and pass variable
            nodeArgs = ()
            nodeKwargs = {}
            if nodeJson['type'] in ('getVar', 'setVar'):
                nodeKwargs['var'] = self.vars[uuid.UUID(nodeJson['varUid'])]
            nodeJson['owningGraphName'] = self.name
            node = getRawNodeInstance(nodeJson['type'], packageName=nodeJson['package'], libName=nodeJson['lib'], *nodeArgs, **nodeKwargs)
            self.addNode(node, nodeJson)

        # restore connections
        graphPins = self.pins
        for nodeJson in jsonData['nodes']:
            for nodeOutputJson in nodeJson['outputs']:
                lhsPin = self.findPin(nodeOutputJson['fullName'])
                for rhsPinFullName in nodeOutputJson['linkedToNames']:
                    rhsPin = self.findPin(rhsPinFullName)
                    connected = connectPins(lhsPin, rhsPin)
                    assert(connected is True), "Failed to restore connection"

    def remove(self):
        """Removes this graph as well as child graphs. Deepest graphs will be removed first
        """
        # graphs should be removed from leafs to root
        for childGraph in set(self.childGraphs):
            childGraph.remove()
        # remove itself
        self.graphManager.removeGraph(self)

    def clear(self):
        """Clears content of this graph as well as child graphs. Deepest graphs will be cleared first
        """
        # graphs should be cleared from leafs to root
        for childGraph in self.childGraphs:
            childGraph.clear()

        # clear itself
        for node in list(self.nodes.values()):
            node.kill()
        self.nodes.clear()

        for var in list(self.vars.values()):
            self.killVariable(var)
        self.vars.clear()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        assert(isinstance(value, str))
        if self.__name != value:
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

    def getNodes(self, classNameFilters=[]):
        """return all nodes without compound's nodes
        """
        if len(classNameFilters) > 0:
            return [n for n in self.nodes.values() if n.__class__.__name__ in classNameFilters]
        else:
            return [n for n in self.nodes.values()]

    @dispatch(str)
    def findNode(self, name):
        for i in self.nodes.values():
            if i.name == name:
                return i
        return None

    @dispatch(uuid.UUID)
    def findNode(self, uuid):
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

        # Check if this node is variable get/set. Variables created in child graphs are not visible to parent ones
        # Do not disrupt variable scope
        if node.__class__.__name__ in ['getVar', 'setVar']:
            var = self.graphManager.findVariable(node.variableUid())
            variableLocation = var.location()
            if len(variableLocation) > len(self.location()):
                return False

        if jsonTemplate is not None:
            jsonTemplate['name'] = self.graphManager.getUniqName(jsonTemplate['name'])
        else:
            node.setName(self.graphManager.getUniqName(node.name))

        self.nodes[node.uid] = node
        node.graph = weakref.ref(self)
        node.postCreate(jsonTemplate)
        return True

    def location(self):
        result = [self.name]
        parent = self._parentGraph
        while parent is not None:
            result.insert(0, parent.name)
            parent = parent.parentGraph
        return result

    def count(self):
        return self.nodes.__len__()

    def plot(self):
        depth = self.depth()
        prefix = "".join(['-'] * depth) if depth > 1 else ''
        parentGraphString = str(None) if self.parentGraph is None else self.parentGraph.name
        print(prefix + "GRAPH:" + self.name + ", parent:{0}".format(parentGraphString))
        # for n in self.getNodes():
        #     print(prefix + "-Node:{}".format(n.name))

        assert(self not in self.childGraphs)

        for child in self.childGraphs:
            child.plot()

import weakref
from blinker import Signal
from multipledispatch import dispatch
from collections import Counter

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow import CreateRawPin
from PyFlow import getRawNodeInstance
from PyFlow import findPinClassByType
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Variable import Variable
from PyFlow.Core.Interfaces import ISerializable


class GraphBase(ISerializable):
    """Data structure representing a nodes graph

    :var graphManager: reference to graph manager
    :vartype graphManager: :class:`~PyFlow.Core.GraphManager.GraphManager`

    :var nameChanged: signal emitted after graph name was changed
    :vartype nameChanged: :class:`~blinker.base.Signal`

    :var categoryChanged: signal emitted after graph category was changed
    :vartype categoryChanged: :class:`~blinker.base.Signal`

    :var childGraphs: a set of child graphs
    :vartype childGraphs: :class:`set`

    :var nodes: nodes storage. Dictionary with :class:`uuid.UUID` as key and :class:`~PyFlow.Core.NodeBase.NodeBase` as value
    :vartype nodes: :class:`dict`

    :var uid: Unique identifier
    :vartype uid: :class:`uuid.UUID`

    .. py:method:: parentGraph
        :property:

        :getter: Returns a reference to parent graph or None if this graph is root

        :setter: Sets new graph as new parent for this graph

    .. py:method:: name
        :property:

        :getter: Returns graph name

        :setter: Sets new graph name and fires signal

    .. py:method:: category
        :property:

        :getter: Returns graph category

        :setter: Sets new graph category and fires signal

    .. py:method:: pins
        :property:

        :getter: Returns dictionary with :class:`uuid.UUID` as key and :class:`~PyFlow.Core.PinBase.PinBase` as value
        :rtype: dict

    """
    def __init__(self, name, manager, parentGraph=None, category='', uid=None, *args, **kwargs):
        super(GraphBase, self).__init__(*args, **kwargs)
        self.graphManager = manager
        self._isRoot = False

        self.nameChanged = Signal(str)
        self.categoryChanged = Signal(str)

        self.__name = name
        self.__category = category

        self._parentGraph = None
        self.childGraphs = set()

        self.parentGraph = parentGraph

        self._nodes = {}
        self._vars = {}
        self.uid = uuid.uuid4() if uid is None else uid

        manager.add(self)

    def setIsRoot(self, bIsRoot):
        """Sets this graph as root

        .. warning:: Used internally

        :param bIsRoot: -- Root or not
        :type bIsRoot: :class:`bool`
        """
        self._isRoot = bIsRoot

    def isRoot(self):
        """Whether this graph is root or not

        :rtype: :class:`bool`
        """
        return self._isRoot

    def getVars(self):
        """Returns this graph's variables storage

        :returns: :class:`uuid.UUID` - :class:`~PyFlow.Core.NodeBase.NodeBase` dict
        :rtype: :class:`dict`
        """
        return self._vars

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
        """Returns depth level of this graph

        :rtype: int
        """
        result = 1
        parent = self._parentGraph
        while parent is not None:
            result += 1
            parent = parent.parentGraph
        return result

    def getVarList(self):
        """return list of variables from active graph

        :rtype: list(:class:`~PyFlow.Core.Variable.Variable`)
        """
        result = list(self._vars.values())
        parent = self._parentGraph
        while parent is not None:
            result += list(parent._vars.values())
            parent = parent.parentGraph
        return result

    def serialize(self, *args, **kwargs):
        """Returns serialized representation of this graph

        :rtype: dict
        """
        result = {
            'name': self.name,
            'category': self.category,
            'vars': [v.serialize() for v in self._vars.values()],
            'nodes': [n.serialize() for n in self._nodes.values()],
            'depth': self.depth(),
            'isRoot': self.isRoot(),
            'parentGraphName': str(self._parentGraph.name) if self._parentGraph is not None else str(None)
        }
        return result

    def populateFromJson(self, jsonData):
        """Populates itself from serialized data

        :param jsonData: serialized graph
        :type jsonData: dict
        """
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
            self._vars[var.uid] = var
        # restore nodes
        for nodeJson in jsonData['nodes']:
            # check if variable getter or setter and pass variable
            nodeArgs = ()
            nodeKwargs = {}
            if nodeJson['type'] in ('getVar', 'setVar'):
                nodeKwargs['var'] = self._vars[uuid.UUID(nodeJson['varUid'])]
            nodeJson['owningGraphName'] = self.name
            node = getRawNodeInstance(nodeJson['type'], packageName=nodeJson['package'], libName=nodeJson['lib'], *nodeArgs, **nodeKwargs)
            self.addNode(node, nodeJson)

        # restore connection
        for nodeJson in jsonData['nodes']:
            for nodeOutputJson in nodeJson['outputs']:
                for linkData in nodeOutputJson['linkedTo']:
                    lhsNode = self.findNode(nodeJson["name"])
                    lhsPin = lhsNode.orderedOutputs[linkData["outPinId"]]
                    rhsNode = self.findNode(linkData["rhsNodeName"])
                    rhsPin = rhsNode.orderedInputs[linkData["inPinId"]]
                    if not arePinsConnected(lhsPin, rhsPin):
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
        for node in list(self._nodes.values()):
            node.kill()
        self._nodes.clear()

        for var in list(self._vars.values()):
            self.killVariable(var)
        self._vars.clear()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        value = str(value)
        if self.__name != value:
            self.__name = value
            self.nameChanged.send(self.__name)

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = str(value)
        self.categoryChanged.send(self.__category)

    def Tick(self, deltaTime):
        """Executed periodically

        :param deltaTime: Elapsed time since last tick
        :type deltaTime: float
        """
        for node in self._nodes.values():
            node.Tick(deltaTime)

    @property
    def pins(self):
        result = {}
        for n in self.getNodesList():
            for pin in tuple(n.inputs.values()) + tuple(n.outputs.values()):
                result[pin.uid] = pin
        return result

    def createVariable(self, dataType=str('AnyPin'), accessLevel=AccessLevel.public, uid=None, name=str("var")):
        """Creates variable inside this graph scope

        :param dataType: Variable data type
        :type dataType: str
        :param accessLevel: Variable access level
        :type accessLevel: :class:`~PyFlow.Core.Common.AccessLevel`
        :param uid: Variable unique identifier
        :type uid: :class:`uuid.UUID`
        :param name: Variable name
        :type name: str
        """
        name = self.graphManager.getUniqVariableName(name)
        var = Variable(self, getPinDefaultValueByType(dataType), name, dataType, accessLevel=accessLevel, uid=uid)
        self._vars[var.uid] = var
        return var

    # TODO: add arguments to deal with references of this var
    # disconnect pins or mark nodes invalid
    def killVariable(self, var):
        """Removes variable from this graph

        :param var: Variable to remove
        :type var: :class:`~PyFlow.Core.Variable.Variable`
        """
        assert(isinstance(var, Variable))
        if var.uid in self._vars:
            popped = self._vars.pop(var.uid)
            popped.killed.send()

    def getNodes(self):
        """Returns this graph's nodes storage

        :rtype: dict(:class:`~PyFlow.Core.NodeBase.NodeBase`)
        """
        return self._nodes

    def getNodesList(self, classNameFilters=[]):
        """Returns this graph's nodes list
        :rtype: list(:class:`~PyFlow.Core.NodeBase.NodeBase`)
        """
        if len(classNameFilters) > 0:
            return [n for n in self._nodes.values() if n.__class__.__name__ in classNameFilters]
        else:
            return [n for n in self._nodes.values()]

    def findNode(self, name):
        """Tries to find node by name

        :param name: Node name
        :type name: str or None
        """
        for i in self._nodes.values():
            if i.name == name:
                return i
        return None

    def getNodesByClassName(self, className):
        """Returns a list of nodes filtered by class name
        :param className: Class name of target nodes
        :type className: str
        :rtype: list(:class:`~PyFlow.Core.NodeBase.NodeBase`)
        """
        nodes = []
        for i in self.getNodesList():
            if i.__class__.__name__ == className:
                nodes.append(i)
        return nodes

    def findPinByUid(self, uid):
        """Tries to find pin by uuid

        :param uid: Unique identifier
        :type uid: :class:`~uuid.UUID`
        :rtype: :class:`~PyFlow.Core.PinBase.PinBase` or None
        """
        pin = None
        if uid in self.pins:
            pin = self.pins[uid]
        return pin

    def findPin(self, pinName):
        """Tries to find pin by name

        :param pinName: String to search by
        :type pinName: str
        :rtype: :class:`~PyFlow.Core.PinBase.PinBase` or None
        """
        result = None
        for pin in self.pins.values():
            if pinName == pin.getFullName():
                result = pin
                break
        return result

    def getInputNode(self):
        """Creates and adds to graph :class:`~PyFlow.Packages.PyFlowBase.Nodes.graphNodes.graphInputs` node

        pins on this node will be exposed on compound node as input pins
        :rtype: :class:`~PyFlow.Core.NodeBase.NodeBase`
        """
        node = getRawNodeInstance("graphInputs", "PyFlowBase")
        self.addNode(node)
        return node

    def getOutputNode(self):
        """Creates and adds to graph :class:`~PyFlow.Packages.PyFlowBase.Nodes.graphNodes.graphOutputs` node.

        pins on this node will be exposed on compound node as output pins
        :rtype: :class:`~PyFlow.Core.NodeBase.NodeBase`
        """
        node = getRawNodeInstance("graphOutputs", "PyFlowBase")
        self.addNode(node)
        return node

    def addNode(self, node, jsonTemplate=None):
        """Adds node to storage

        :param node: Node to add
        :type node: NodeBase
        :param jsonTemplate: serialized representation of node. This used when graph deserialized to do custom stuff after node will be added.
        :type jsonTemplate: dict
        :rtype: bool
        """
        assert(node is not None), "failed to add node, None is passed"
        if node.uid in self._nodes:
            return False

        # Check if this node is variable get/set. Variables created in child graphs are not visible to parent ones
        # Do not disrupt variable scope
        if node.__class__.__name__ in ['getVar', 'setVar']:
            var = self.graphManager.findVariableByUid(node.variableUid())
            variableLocation = var.location()
            if len(variableLocation) > len(self.location()):
                return False
            if len(variableLocation) == len(self.location()):
                if Counter(variableLocation) != Counter(self.location()):
                    return False

        node.graph = weakref.ref(self)
        if jsonTemplate is not None:
            jsonTemplate['name'] = self.graphManager.getUniqName(jsonTemplate['name'])
        else:
            node.setName(self.graphManager.getUniqName(node.name))

        self._nodes[node.uid] = node
        node.postCreate(jsonTemplate)
        return True

    def location(self):
        """Returns path to current location in graph tree

        Example:

        >>> ["root", "compound1", "compound2"]

        means:

        >>> # root
        >>> # |- compound
        >>> #    |- compound2

        :rtype: list(str)
        """
        result = [self.name]
        parent = self._parentGraph
        while parent is not None:
            result.insert(0, parent.name)
            parent = parent.parentGraph
        return result

    def count(self):
        """Returns number of nodes

        :rtype: int
        """
        return self._nodes.__len__()

    def plot(self):
        """Prints graph to console. May be useful for debugging
        """
        depth = self.depth()
        prefix = "".join(['-'] * depth) if depth > 1 else ''
        parentGraphString = str(None) if self.parentGraph is None else self.parentGraph.name
        print(prefix + "GRAPH:" + self.name + ", parent:{0}".format(parentGraphString))

        assert(self not in self.childGraphs)

        for child in self.childGraphs:
            child.plot()

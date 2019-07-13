import os
import json
import weakref
from copy import deepcopy

from blinker import Signal

from PyFlow.Core import NodeBase
from PyFlow.Core import GraphBase
from PyFlow.Core.Common import *


class compound(NodeBase):
    """this node encapsulates a graph, like compound in xsi

    pins can be edited only from inside the compound
    """
    def __init__(self, name):
        super(compound, self).__init__(name)
        self.isCompoundNode = True
        self.pinExposed = Signal(object)
        self._rawGraph = None
        self.__inputsMap = {}
        self.__outputsMap = {}
        self.bCacheEnabled = False

    @property
    def inputsMap(self):
        return self.__inputsMap

    @property
    def outputsMap(self):
        return self.__outputsMap

    @property
    def rawGraph(self):
        return self._rawGraph

    @rawGraph.setter
    def rawGraph(self, newGraph):
        assert(newGraph is not None)
        self._rawGraph = newGraph

    def syncPins(self):
        # look for graph nodes pins was added
        nodeInputPins = self.namePinInputsMap
        nodeOutputPins = self.namePinOutputsMap

        graphInputsNodes = self.rawGraph.getNodesList(classNameFilters=['graphInputs'])
        graphInputPins = {}
        for graphInputNode in graphInputsNodes:
            for outPin in graphInputNode.orderedOutputs.values():
                graphInputPins[outPin.name] = outPin
                # create companion pin if needed
                if outPin.name not in nodeInputPins:
                    self.onGraphInputPinCreated(outPin)

        graphOutputNodes = self.rawGraph.getNodesList(classNameFilters=['graphOutputs'])
        graphOutputPins = {}
        for graphOutputNode in graphOutputNodes:
            for inPin in graphOutputNode.orderedInputs.values():
                graphOutputPins[inPin.name] = inPin
                # create companion pin if needed
                if inPin.name not in nodeOutputPins:
                    self.onGraphOutputPinCreated(inPin)

        for nodeInputPinName, nodeInputPin in nodeInputPins.items():
            if nodeInputPinName not in graphInputPins:
                if nodeInputPin in self.__inputsMap:
                    nodeInputPin.kill()
                    clearSignal(nodeInputPin.killed)
                    self.__inputsMap.pop(nodeInputPin)

        for nodeOutputPinName, nodeOutputPin in nodeOutputPins.items():
            if nodeOutputPinName not in graphOutputPins:
                if nodeOutputPin in self.__outputsMap:
                    nodeOutputPin.kill()
                    clearSignal(nodeOutputPin.killed)
                    self.__outputsMap.pop(nodeOutputPin)

    def Tick(self, delta):
        self.syncPins()
        self.rawGraph.Tick(delta)
        super(compound, self).Tick(delta)

    def setName(self, name):
        super(compound, self).setName(name)
        if self.rawGraph is not None:
            self.rawGraph.name = self.getName()

    @staticmethod
    def category():
        return 'SubGraphs'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Encapsulate a graph inside a node'

    def serialize(self):
        default = NodeBase.serialize(self)
        default['graphData'] = self.rawGraph.serialize()
        return default

    def onGraphInputPinCreated(self, outPin):
        """Reaction when pin added to graphInputs node

        :param outPin: output pin on graphInputs node
        :type outPin: :class:`~PyFlow.Core.PinBase.PinBase`
        """

        # add companion pin for graphInputs node's output pin
        subgraphInputPin = self.createInputPin(outPin.name,
                                               outPin.__class__.__name__,
                                               outPin.defaultValue(),
                                               outPin.call,
                                               outPin.structureType,
                                               outPin.constraint,
                                               outPin.structConstraint,
                                               group=outPin.owningNode().name)
        if subgraphInputPin.isAny():
            subgraphInputPin.supportedDataTypes = outPin.supportedDataTypes
            subgraphInputPin.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)

        outPin.owningNode().constraints[outPin.constraint].append(subgraphInputPin)
        self.constraints[outPin.constraint].append(outPin)

        outPin.owningNode().structConstraints[outPin.structConstraint].append(subgraphInputPin)
        self.structConstraints[outPin.structConstraint].append(outPin)

        self.__inputsMap[subgraphInputPin] = outPin
        pinAffects(subgraphInputPin, outPin)
        # connect

        def forceRename(name):
            subgraphInputPin.setName(name, force=True)
        outPin.nameChanged.connect(forceRename, weak=False)

        # broadcast for UI wrapper class
        self.pinExposed.send(subgraphInputPin)

    def onGraphOutputPinCreated(self, inPin):
        """Reaction when pin added to graphOutputs node

        :param inPin: input pin on graphOutputs node
        :type inPin: :class:`~PyFlow.Core.PinBase.PinBase`
        """

        # add companion pin for graphOutputs node's input pin
        subgraphOutputPin = self.createOutputPin(inPin.name,
                                                 inPin.__class__.__name__,
                                                 inPin.defaultValue(),
                                                 inPin.structureType,
                                                 inPin.constraint,
                                                 inPin.structConstraint,
                                                 group=inPin.owningNode().name)
        if subgraphOutputPin.isAny():
            subgraphOutputPin.supportedDataTypes = inPin.supportedDataTypes
            subgraphOutputPin.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)

        if subgraphOutputPin.isExec():
            inPin.onExecute.connect(subgraphOutputPin.call)

        inPin.owningNode().constraints[inPin.constraint].append(subgraphOutputPin)
        self.constraints[inPin.constraint].append(inPin)

        inPin.owningNode().structConstraints[inPin.structConstraint].append(subgraphOutputPin)
        self.structConstraints[inPin.structConstraint].append(inPin)

        self.__outputsMap[subgraphOutputPin] = inPin
        pinAffects(inPin, subgraphOutputPin)

        # connect
        def forceRename(name):
            subgraphOutputPin.setName(name, force=True)
        inPin.nameChanged.connect(forceRename, weak=False)

        # broadcast for UI wrapper class
        self.pinExposed.send(subgraphOutputPin)

    def kill(self, *args, **kwargs):
        self.rawGraph.remove()
        super(compound, self).kill(*args, **kwargs)

    def postCreate(self, jsonTemplate=None):
        super(compound, self).postCreate(jsonTemplate=jsonTemplate)

        if jsonTemplate is not None and 'graphData' in jsonTemplate:
            parentGraph = self.graph().graphManager.findGraph(jsonTemplate['owningGraphName'])
            self.rawGraph = GraphBase(self.name, self.graph().graphManager, parentGraph)
            # recreate graph contents
            jsonTemplate['graphData']['name'] = self.getName()
            self.rawGraph.populateFromJson(jsonTemplate['graphData'])

            self.syncPins()

            inputsMap = self.namePinInputsMap
            for inpJson in jsonTemplate['inputs']:
                inputsMap[inpJson['name']].uid = uuid.UUID(inpJson['uuid'])

            outputsMap = self.namePinOutputsMap
            for outJson in jsonTemplate['outputs']:
                outputsMap[outJson['name']].uid = uuid.UUID(outJson['uuid'])
        else:
            self.rawGraph = GraphBase(self.name, self.graph().graphManager, self.graph().graphManager.activeGraph())

    def addNode(self, node):
        self.rawGraph.addNode(node)

    def autoAffectPins(self):
        pass

    def compute(self, *args, **kwargs):
        # put data from inner graph pins to outer compound node output companions
        for outputPin, innerPin in self.__outputsMap.items():
            outputPin.setData(innerPin.getData())

## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.Core.Common import *
from PyFlow.Core.Interfaces import IEvaluationEngine


class DefaultEvaluationEngine_Impl(IEvaluationEngine):
    """Default evaluation engine implementation
    """

    def __init__(self):
        super(DefaultEvaluationEngine_Impl, self).__init__()

    @staticmethod
    def getPinData(pin):
        if not pin.hasConnections():
            return pin.currentData()

        bOwningNodeCallable = pin.owningNode().bCallable

        if not pin.dirty:
            return pin.currentData()
        
        order = DefaultEvaluationEngine_Impl.getEvaluationOrderIterative(pin.owningNode())
        [node.processNode() for node in order]

        if not pin.dirty:
            pin.owningNode().processNode()
        return pin.currentData()

    @staticmethod
    def getEvaluationOrderIterative(node, forward=False):
        visited = set()
        stack = [node]
        order = []
        while len(stack):
            node = stack[-1]
            stack.pop()

            if node not in visited:
                order.insert(0, node)
                visited.add(node)
            if not forward:
                lhsNodes = DefaultEvaluationEngine_Impl().getNextLayerNodes(node)
            else:
                lhsNodes = DefaultEvaluationEngine_Impl().getForwardNextLayerNodes(node)
            for n in lhsNodes:
                if n not in visited:
                    stack.append(n)
        order.pop()
        return order

    @staticmethod
    def getEvaluationOrder(node):
        visited = set()
        order = []

        def dfsWalk(n):
            visited.add(n)
            nextNodes = DefaultEvaluationEngine_Impl.getNextLayerNodes(n)
            for lhsNode in nextNodes:
                if lhsNode not in visited:
                    dfsWalk(lhsNode)
            order.append(n)

        dfsWalk(node)
        order.pop()
        return order

    @staticmethod
    def getNextLayerNodes(node):
        nodes = set()
        nodeInputs = node.inputs

        if not len(nodeInputs) == 0:
            for inputPin in nodeInputs.values():
                if not len(inputPin.affected_by) == 0:
                    # check if it is compound node and dive in
                    affectedByPins = set()
                    for pin in inputPin.affected_by:
                        if pin.owningNode().isCompoundNode:
                            innerPin = pin.owningNode().outputsMap[pin]
                            affectedByPins.add(innerPin)
                        else:
                            affectedByPins.add(pin)

                    for outPin in affectedByPins:
                        outPinNode = outPin.owningNode()
                        if not outPinNode.bCallable:
                            # if node.isDirty():
                            nodes.add(outPinNode)
        elif node.__class__.__name__ == "graphInputs":
            # graph inputs node
            for subgraphInputPin in node.outputs.values():
                for outPin in subgraphInputPin.affected_by:
                    owningNode = outPin.owningNode()
                    nodes.add(owningNode)
        return nodes

    @staticmethod
    def getForwardNextLayerNodes(node):
        nodes = set()
        nodeOutputs = node.outputs

        if not len(nodeOutputs) == 0:
            for outputPin in nodeOutputs.values():
                if not len(outputPin.affects) == 0:
                    # check if it is compound node and dive in
                    affectedByPins = set()
                    for pin in outputPin.affects:
                        if pin.owningNode().isCompoundNode:
                            innerPin = pin.owningNode().inputsMap[pin]
                            affectedByPins.add(innerPin)
                        else:
                            affectedByPins.add(pin)

                    for inPin in affectedByPins:
                        inPinNode = inPin.owningNode()
                        if not inPinNode.bCallable:
                            nodes.add(inPinNode)
        elif node.__class__.__name__ == "graphOutputs":
            # graph inputs node
            for subgraphInputPin in node.inputs.values():
                for outPin in subgraphInputPin.affects:
                    owningNode = outPin.owningNode()
                    nodes.add(owningNode)
        return nodes


@SingletonDecorator
class EvaluationEngine(object):
    def __init__(self):
        self._impl = DefaultEvaluationEngine_Impl()

    def getPinData(self, pin):
        return self._impl.getPinData(pin)

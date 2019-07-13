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

        if not bOwningNodeCallable:
            return pin.currentData()

        compute_order = DefaultEvaluationEngine_Impl.getEvaluationOrder(pin.owningNode())
        for layerIndex in reversed(list(compute_order.keys())):
            nodeList = compute_order[layerIndex]
            # this for loop can be parallel
            for node in nodeList:
                node.processNode()

        if not bOwningNodeCallable:
            pin.owningNode().processNode()
        return pin.currentData()

    @staticmethod
    def getEvaluationOrder(node):

        order = {0: []}

        # include first node only if it is callable
        if not node.bCallable:
            order[0].append(node)

        def foo(n):
            next_layer_nodes = DefaultEvaluationEngine_Impl.getNextLayerNodes(n)
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
                            nodes.add(outPinNode)
        elif node.__class__.__name__ == "graphInputs":
            # graph inputs node
            for subgraphInputPin in node.outputs.values():
                for outPin in subgraphInputPin.affected_by:
                    owningNode = outPin.owningNode()
                    # if owningNode.isCompoundNode:
                    #     continue
                    nodes.add(owningNode)
        return nodes


@SingletonDecorator
class EvaluationEngine(object):
    def __init__(self):
        self._impl = DefaultEvaluationEngine_Impl()

    def getPinData(self, pin):
        return self._impl.getPinData(pin)

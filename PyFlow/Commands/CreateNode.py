"""
base class for all commands. Use this to implement your own
"""

from Qt.QtWidgets import QUndoCommand
import Nodes
import FunctionLibraries
from Node import Node


def getNodeInstance(module, class_name, nodeName, graph):
    # Check in Nodes module first
    mod = Nodes.getNode(class_name)
    if mod is not None:
        instance = mod(nodeName, graph)
        return instance

    # if not found - continue searching in FunctionLibraries
    foo = FunctionLibraries.findFunctionByName(class_name)
    if foo:
        instance = Node.initializeFromFunction(foo, graph)
        return instance
    return None


class CreateNode(QUndoCommand):

    def __init__(self, graph, jsonTemplate):
        super(CreateNode, self).__init__()
        self.graph = graph
        self.nodeInstance = None
        self.jsonTemplate = jsonTemplate
        self.setText("create {} node".format(jsonTemplate['type']))

    def undo(self):
        self.graph.scene().blockSignals(True)
        self.jsonTemplate = self.nodeInstance.serialize()
        self.nodeInstance.kill()
        self.graph.scene().blockSignals(False)

    def redo(self):
        self.graph.scene().blockSignals(True)
        self.nodeInstance = getNodeInstance(Nodes, self.jsonTemplate['type'], self.jsonTemplate['name'], self.graph)

        # if no such node in Nodes mod, check Function libs
        if self.nodeInstance is None:
            foo = FunctionLibraries.findFunctionByName(self.jsonTemplate['type'])
            if foo:
                self.nodeInstance = Node.initializeFromFunction(foo, self.graph)

        # If clas still not found, check variables
        if self.nodeInstance is None:
            if self.jsonTemplate['type'] == 'GetVarNode':
                self.nodeInstance = self.graph.createVariableGetter(self.jsonTemplate)
            if self.jsonTemplate['type'] == 'SetVarNode':
                self.nodeInstance = self.graph.createVariableSetter(self.jsonTemplate)

        if self.nodeInstance is None:
            raise ValueError("node class not found!")

        self.graph.addNode(self.nodeInstance, self.jsonTemplate)
        self.graph.scene().blockSignals(False)

from Qt.QtWidgets import QUndoCommand
import Nodes
import FunctionLibraries
from Node import Node
import uuid
from AbstractGraph import *


class CreateNode(QUndoCommand):

    def __init__(self, graph, jsonTemplate):
        super(CreateNode, self).__init__()
        self.graph = graph
        self.nodeInstance = None
        self.jsonTemplate = jsonTemplate
        self.setText("create {} node".format(jsonTemplate['type']))
        self.uid = None

    def undo(self):
        self.graph.scene().blockSignals(True)
        self.jsonTemplate = self.nodeInstance.serialize()
        self.graph.nodes[uuid.UUID(self.jsonTemplate['uuid'])].kill()
        self.graph.scene().blockSignals(False)

    def redo(self):
        self.graph.scene().blockSignals(True)
        self.nodeInstance = self.graph._createNode(self.jsonTemplate)
        # self.nodeInstance.uid = uuid.UUID(self.jsonTemplate['uuid'])
        if self.uid:
            self.nodeInstance.uid = self.uid
        else:
            self.uid = self.nodeInstance.uid

        self.graph.scene().blockSignals(False)

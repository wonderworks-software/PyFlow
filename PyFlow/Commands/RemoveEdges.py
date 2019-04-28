from uuid import UUID

from Qt.QtWidgets import QUndoCommand

from PyFlow.UI.Canvas.UIConnection import UIConnection


class RemoveEdges(QUndoCommand):
    '''
    Disconnects pins
    '''

    def __init__(self, graph, jsonTemplates):
        super(RemoveEdges, self).__init__()
        self.setText('Remove connections')
        self.jsonTemplates = jsonTemplates
        self.graph = graph

    def undo(self):
        for edgeJson in self.jsonTemplates:
            UIConnection.deserialize(edgeJson, self.graph)

    def redo(self):
        for edgeJson in self.jsonTemplates:
            uid = UUID(edgeJson['uuid'])
            if uid in self.graph.connections:
                self.graph.removeConnection(self.graph.connections[uid])

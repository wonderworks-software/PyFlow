import uuid

from Qt.QtWidgets import QUndoCommand


class CreateNode(QUndoCommand):
    '''
    Creates a node
    '''
    def __init__(self, graph, jsonTemplate):
        super(CreateNode, self).__init__()
        self.graph = graph
        self.nodeInstance = None
        self.jsonTemplate = jsonTemplate
        self.setText("create {} node".format(jsonTemplate['type']))
        self.uid = uuid.UUID(jsonTemplate['uuid'])

    def undo(self):
        self.graph.scene().blockSignals(True)

        self.jsonTemplate.clear()
        self.jsonTemplate = self.nodeInstance.serialize()
        self.graph.nodes[self.uid].kill()
        self.graph.scene().blockSignals(False)

    def redo(self):
        self.graph.scene().blockSignals(True)
        self.jsonTemplate['uuid'] = str(self.uid)
        self.nodeInstance = self.graph._createNode(self.jsonTemplate)
        self.graph.scene().blockSignals(False)

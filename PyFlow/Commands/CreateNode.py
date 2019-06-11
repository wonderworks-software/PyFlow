import uuid
from nine import str

from Qt.QtWidgets import QUndoCommand


class CreateNode(QUndoCommand):
    def __init__(self, canvas, jsonTemplate, **kwargs):
        super(CreateNode, self).__init__()
        self.kwargs = kwargs
        self.canvas = canvas
        self.nodeInstance = None
        self.jsonTemplate = jsonTemplate
        self.setText("create {} node".format(jsonTemplate['type']))
        self.uid = uuid.UUID(jsonTemplate['uuid'])

    def undo(self):
        self.canvas.scene().blockSignals(True)

        self.jsonTemplate.clear()
        self.jsonTemplate = self.nodeInstance.serialize()
        self.canvas.nodes[self.uid]._rawNode.kill()
        self.canvas.scene().blockSignals(False)

    def redo(self):
        self.canvas.scene().blockSignals(True)
        self.jsonTemplate['uuid'] = str(self.uid)
        self.nodeInstance = self.canvas._createNode(self.jsonTemplate, **self.kwargs)
        self.canvas.scene().blockSignals(False)

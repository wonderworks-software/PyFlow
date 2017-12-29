from Qt.QtWidgets import QUndoCommand


class Select(QUndoCommand):

    def __init__(self, nodeUids, graph):
        super(Select, self).__init__()
        self.setText("Select nodes")
        self.nodeUids = nodeUids
        self.graph = graph

    def undo(self):
        # self.graph.scene().blockSignals(True)

        for uid in self.nodeUids:
            if uid in self.graph.nodes:
                self.graph.nodes[uid].setSelected(False)

        # self.graph.scene().blockSignals(False)

    def redo(self):
        # self.graph.scene().blockSignals(True)

        for uid in self.nodeUids:
            if uid in self.graph.nodes:
                self.graph.nodes[uid].setSelected(True)

        # self.graph.scene().blockSignals(False)

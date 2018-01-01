from Qt.QtWidgets import QUndoCommand
from AbstractGraph import Graph
from AbstractGraph import PinTypes
from Edge import Edge


class ConnectPin(QUndoCommand):

    def __init__(self, graph, src, dst):
        super(ConnectPin, self).__init__()
        self.graph = graph
        self.srcUid = src.uid
        self.dstUid = dst.uid
        self.setText('connect edges')
        self.edgeUid = None

    def undo(self):
        self.graph.scene().blockSignals(True)

        self.graph.removeEdge(self.graph.edges[self.edgeUid])

        self.graph.scene().blockSignals(False)

    def redo(self):

        self.graph.scene().blockSignals(True)

        src = self.graph.pins[self.srcUid]
        dst = self.graph.pins[self.dstUid]
        edge = self.graph._addEdge(src, dst)

        if edge and self.edgeUid:
            edge.uid = self.edgeUid

        self.edgeUid = edge.uid

        self.graph.scene().blockSignals(False)

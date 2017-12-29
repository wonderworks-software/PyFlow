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
        self.setText('connect {0} to {1}'.format(src.pinName(), dst.pinName()))
        self.edgeUid = None

    def undo(self):
        self.graph.scene().blockSignals(True)

        if self.edgeUid:
            if self.edgeUid in self.graph.edges:
                self.graph.removeEdge(self.graph.edges[self.edgeUid])
                self.edgeUid = None

        self.graph.scene().blockSignals(False)

    def redo(self):
        self.graph.scene().blockSignals(True)

        src = self.graph.pins[self.srcUid]
        dst = self.graph.pins[self.dstUid]
        edge = self.graph._addEdge(src, dst)
        if edge:
            self.edgeUid = edge.uid

        self.graph.scene().blockSignals(False)

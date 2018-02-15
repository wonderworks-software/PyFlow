from Qt.QtWidgets import QUndoCommand


class ConnectPin(QUndoCommand):
    '''
    Connects two pins
    '''
    def __init__(self, graph, src, dst):
        super(ConnectPin, self).__init__()
        self.graph = graph
        self.srcUid = src.uid
        self.dstUid = dst.uid
        self.setText('connect edges')
        self.edgeUid = None

    def undo(self):
        if self.edgeUid in self.graph.edges:
            self.graph.scene().blockSignals(True)
            self.graph.removeEdge(self.graph.edges[self.edgeUid])
            self.graph.scene().blockSignals(False)

    def redo(self):

        self.graph.scene().blockSignals(True)

        src = self.graph.pins[self.srcUid]
        dst = self.graph.pins[self.dstUid]
        edge = self.graph._addEdge(src, dst)

        # recreate the same edge with same uuid
        # if it was deleted
        if edge and self.edgeUid:
            edge.uid = self.edgeUid

        # if first created store connection uuid
        # of this particular connection
        if edge and self.edgeUid is None:
            self.edgeUid = edge.uid

        self.graph.scene().blockSignals(False)

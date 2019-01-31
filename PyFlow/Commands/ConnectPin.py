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

        srcPin = self.graph.findUIPinByUID(self.srcUid)
        if srcPin is None:
            print(self.srcUid, "not found")

        dstPin = self.graph.findUIPinByUID(self.dstUid)
        if dstPin is None:
            print(self.dstUid, "not found")

        edge = self.graph._addEdge(srcPin, dstPin)

        # recreate the same edge with same uuid
        # if it was deleted
        if edge and self.edgeUid:
            edge.uid = self.edgeUid

        # if first created store connection uuid
        # of this particular connection
        if edge and self.edgeUid is None:
            self.edgeUid = edge.uid

        self.graph.scene().blockSignals(False)

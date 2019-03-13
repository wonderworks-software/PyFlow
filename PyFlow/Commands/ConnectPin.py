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
        self.setText('connect connections')
        self.edgeUid = None

    def undo(self):
        if self.edgeUid in self.graph.connections:
            self.graph.scene().blockSignals(True)
            self.graph.removeEdge(self.graph.connections[self.edgeUid])
            self.graph.scene().blockSignals(False)

    def redo(self):
        self.graph.scene().blockSignals(True)

        srcPin = self.graph.findUIPinByUID(self.srcUid)
        if srcPin is None:
            print(self.srcUid, "not found")

        dstPin = self.graph.findUIPinByUID(self.dstUid)
        if dstPin is None:
            print(self.dstUid, "not found")

        connection = self.graph._addConnection(srcPin, dstPin)

        # recreate the same connection with same uuid
        # if it was deleted
        if connection and self.edgeUid:
            connection.uid = self.edgeUid

        # if first created store connection uuid
        # of this particular connection
        if connection and self.edgeUid is None:
            self.edgeUid = connection.uid

        self.graph.scene().blockSignals(False)

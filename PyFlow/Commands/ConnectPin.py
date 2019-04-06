from Qt.QtWidgets import QUndoCommand


class ConnectPin(QUndoCommand):
    '''
    Connects two pins
    '''
    def __init__(self, canvas, src, dst):
        super(ConnectPin, self).__init__()
        self.canvas = canvas
        self.srcUid = src.uid
        self.dstUid = dst.uid
        self.setText('connect connections')
        self.edgeUid = None

    def undo(self):
        if self.edgeUid in self.canvas.connections:
            self.canvas.scene().blockSignals(True)
            self.canvas.removeConnection(self.canvas.connections[self.edgeUid])
            self.canvas.scene().blockSignals(False)

    def redo(self):
        self.canvas.scene().blockSignals(True)

        srcPin = self.canvas.findPin(self.srcUid)
        if srcPin is None:
            return

        dstPin = self.canvas.findPin(self.dstUid)
        if dstPin is None:
            return

        connection = self.canvas.connectPinsInternal(srcPin, dstPin)

        # recreate the same connection with same uuid
        # if it was deleted
        if connection and self.edgeUid:
            connection.uid = self.edgeUid

        # if first created store connection uuid
        # of this particular connection
        if connection and self.edgeUid is None:
            self.edgeUid = connection.uid

        self.canvas.scene().blockSignals(False)

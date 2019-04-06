from uuid import UUID

from Qt.QtWidgets import QUndoCommand


class RemoveNodes(QUndoCommand):
    '''
    Removes nodes
    '''
    def __init__(self, selectedNodes, graph):
        super(RemoveNodes, self).__init__()
        self.setText("Remove nodes")
        self.graph = graph
        self.connectionInfo = []
        self.serializedNodes = []
        # we do not want to use class references directly
        # instead we store uuids, and access refs through graph
        for node in selectedNodes:
            self.serializedNodes.append(node.serialize())

    def undo(self):
        for nodeJson in self.serializedNodes:
            nodeInstance = self.graph._createNode(nodeJson)
            nodeInstance.uid = UUID(nodeJson['uuid'])
        # restore connection info
        for edgeJson in self.connectionInfo:
            src = self.graph.findPin(UUID(edgeJson['sourceUUID']))
            dst = self.graph.findPin(UUID(edgeJson['destinationUUID']))
            connection = self.graph.connectPinsInternal(src, dst)
            if connection:
                connection.uid = UUID(edgeJson['uuid'])

    def redo(self):
        for nodeData in self.serializedNodes:
            uid = UUID(nodeData['uuid'])
            if uid in self.graph.nodes:
                node = self.graph.nodes[uid]

                # store connecton info
                for pin in list(node.UIinputs.values()) + list(node.UIoutputs.values()):
                    for e in pin.connections:
                        self.connectionInfo.append(e.serialize())

                node._rawNode.kill()

            else:
                assert(False), "node {} not in graph".format(uid)

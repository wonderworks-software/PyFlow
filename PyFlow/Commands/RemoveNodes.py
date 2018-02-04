from Qt.QtWidgets import QUndoCommand
from uuid import UUID


class RemoveNodes(QUndoCommand):

    def __init__(self, selectedNodes, graph):
        super(RemoveNodes, self).__init__()
        self.setText("Remove nodes")
        self.graph = graph
        self.selectedNodes = selectedNodes
        self.connectionInfo = []
        self.jsonData = []
        # we do not want to use class references directly
        # instead we store uuids, and access refs through graph
        for node in self.selectedNodes:
            self.jsonData.append(node.serialize())

    def undo(self):
        for nodeJson in self.jsonData:
            nodeInstance = self.graph._createNode(nodeJson)
            nodeInstance.uid = UUID(nodeJson['uuid'])
        # restore connection info
        for edgeJson in self.connectionInfo:
            src = self.graph.pins[UUID(edgeJson['sourceUUID'])]
            dst = self.graph.pins[UUID(edgeJson['destinationUUID'])]
            edge = self.graph._addEdge(src, dst)
            if edge:
                edge.uid = UUID(edgeJson['uuid'])

    def redo(self):
        for nodeData in self.jsonData:
            uid = UUID(nodeData['uuid'])
            if uid in self.graph.nodes:
                node = self.graph.nodes[uid]

                # store connecton info
                for pin in node.inputs.values() + node.outputs.values():
                    for e in pin.edge_list:
                        self.connectionInfo.append(e.serialize())
                    pin.disconnectAll()

                node.kill()

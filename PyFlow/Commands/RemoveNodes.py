from Qt.QtWidgets import QUndoCommand
from Node import Node
from Edge import Edge
from uuid import UUID


class RemoveNodes(QUndoCommand):

    def __init__(self, selectedNodesData, graph):
        super(RemoveNodes, self).__init__()
        self.setText("Remove nodes")
        self.graph = graph
        self.selectedNodesData = selectedNodesData
        self.connectionInfo = []

    def undo(self):
        for nodeJson in self.selectedNodesData:
            nodeInstance = self.graph._createNode(nodeJson)
            nodeInstance.uid = UUID(nodeJson['uuid'])
        # restore connection info
        for edgeJson in self.connectionInfo:
            src = self.graph.pins[UUID(edgeJson['sourceUUID'])]
            dst = self.graph.pins[UUID(edgeJson['destinationUUID'])]
            self.graph._addEdge(src, dst)

    def redo(self):
        for nodeJson in self.selectedNodesData:
            uid = UUID(nodeJson['uuid'])
            node = self.graph.nodes[uid]

            # store connecton info
            for pin in node.inputs.values() + node.outputs.values():
                for e in pin.edge_list:
                    self.connectionInfo.append(e.serialize())

            self.graph.nodes[uid].kill()

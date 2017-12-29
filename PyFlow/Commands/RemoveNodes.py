from Qt.QtWidgets import QUndoCommand
from Node import Node
from Edge import Edge
from uuid import UUID


class RemoveNodes(QUndoCommand):

    def __init__(self, selectedNodes, graph):
        super(RemoveNodes, self).__init__()
        self.setText("Remove nodes")
        self.graph = graph
        self.selectedNodes = selectedNodes
        self.jsonData = []
        self.connectionInfo = []
        for node in self.selectedNodes:
            self.jsonData.append(node.serialize())

    def undo(self):
        for nodeJson in self.jsonData:
            nodeInstance = self.graph._createNode(nodeJson)
            # nodeInstance.postCreate(nodeJson)
            nodeInstance.uid = UUID(nodeJson['uuid'])
        # restore connection info
        for edgeJson in self.connectionInfo:
            srcUid = edgeJson['sourceUUID']
            dstUid = edgeJson['destinationUUID']
            self.graph._addEdge(self.graph.pins[UUID(srcUid)], self.graph.pins[UUID(dstUid)])

    def redo(self):

        # del self.jsonData[:]
        # for node in self.selectedNodes:
        #     self.jsonData.append(node.serialize())

        for nodeJson in self.jsonData:
            uid = UUID(nodeJson['uuid'])
            node = self.graph.nodes[uid]

            # store connecton info
            for pin in node.inputs.values() + node.outputs.values():
                for e in pin.edge_list:
                    self.connectionInfo.append(e.serialize())

            self.graph.nodes[uid].kill()

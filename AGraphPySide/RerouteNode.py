from Settings import *
from PySide import QtGui
from PySide import QtCore


class RerouteNode(QtGui.QGraphicsEllipseItem, Colors):
    def __init__(self, x, y, w, h, parent, scene, graph):
        QtGui.QGraphicsEllipseItem.__init__(self, parent, scene)
        self.setRect(x, y, w, h)
        self.graph = graph
        self.setPen(QtGui.QPen(self.kConnectionLines, 1.0, QtCore.Qt.SolidLine))
        self.setBrush(QtGui.QBrush(self.kConnectionLines))
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.left_edge = None
        self.right_edge = None

    def kill(self):
        try:
            if self.left_edge:
                self.graph.edges.remove(self.left_edge)
                self.graph.scene_widget.removeItem(self.left_edge)
        except:
            pass

        try:
            if self.right_edge:
                self.graph.edges.remove(self.right_edge)
                self.graph.scene_widget.removeItem(self.right_edge)
        except:
            pass

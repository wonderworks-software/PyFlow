from PySide import QtCore
from PySide import QtGui
import math
from BaseNode import Node
from Settings import Colors
from AbstractGraph import *
from Edge import Edge


class SceneClass(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.Type = 'SCENE'
        self.setItemIndexMethod(self.NoIndex)
        self.setParent(parent)
        self.pressed_port = None

    def mouseMoveEvent(self, event):
        super(SceneClass, self).mouseMoveEvent(event)


class GraphWidget(QtGui.QGraphicsView, Colors, AGraph):

    def __init__(self, name):
        QtGui.QGraphicsView.__init__(self)
        AGraph.__init__(self, name)
        self.pressed_item = None
        self.released_item = None
        self._isPanning = False
        self._mousePressed = False
        self.timerId = 0
        self.scale(2.0, 2.0)
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.scene_widget = SceneClass(self)
        self.scene_widget.setSceneRect(self.viewport().rect())
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.factor = 1
        self.scale(self.factor, self.factor)
        self.setMinimumSize(800, 600)
        self.setWindowTitle(self.tr(name))

    def itemMoved(self):

        pass

    def keyPressEvent(self, event):

        QtGui.QGraphicsView.keyPressEvent(self, event)

    def mousePressEvent(self,  event):

        self.pressed_item = self.itemAt(event.pos())
        if event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(GraphWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.released_item = self.itemAt(event.pos())
        p_itm = self.pressed_item
        r_itm = self.released_item
        do_connect = True
        for i in [p_itm, r_itm]:
            if not i:
                do_connect = False
                break
            if not hasattr(i, 'object_type'):
                do_connect = False
                break
            if not i.object_type == AGObjectTypes.tPort:
                do_connect = False
                break
        if do_connect:
            self.add_edge(p_itm, r_itm)

        super(GraphWidget, self).mouseReleaseEvent(event)

    def timerEvent(self, event):

        nodes = [item for item in self.scene().items() if isinstance(item, Node)]

        for node in nodes:
            node.update()

    def wheelEvent(self, event):

        self.scale_view(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):

        # Shadow.
        scene_rect = self.sceneRect()
        # Fill.
        gradient = self.kSceneBackground
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen())
        painter.drawRect(scene_rect)

    def add_node(self, node):

        AGraph.add_node(self, node)
        self.scene_widget.addItem(node)

    def add_edge(self, p1, p2):

        debug = self.is_debug()
        if p1.type == AGPortTypes.kInput:
            src = p2
            dst = p1
        else:
            src = p1
            dst = p2

        if src in dst.affected_by:
            if debug:
                print 'already connected. skipped'
            return
        if src.type == dst.type:
            if debug:
                print 'same types can not be connected'
            return
        if src.parent == dst.parent:
            if debug:
                print 'can not connect to self'
            return

        edge = Edge(src, dst)
        portAffects(src, dst)

        src._data = dst._data

        self.scene().addItem(edge)
        self.edges.append(edge)
        src.edge_list.append(edge)
        dst.edge_list.append(edge)
        src.set_dirty()
        return edge

    def remove_edge(self, edge):

        edge.destination.affected_by.remove(edge.source)
        edge.source.affects.remove(edge.destination)
        edge.destination.edge_list.remove(edge)
        edge.source.edge_list.remove(edge)
        self.edges.remove(edge)
        self.scene().removeItem(edge)

    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if self.factor < 0.3 or self.factor > 5:
            return

        self.scale(scale_factor, scale_factor)

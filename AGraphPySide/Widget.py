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
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scene_widget.setSceneRect(QtCore.QRect(-2500, -2500, 2500, 2500))
        self.factor = 1
        self.scale(self.factor, self.factor)
        self.setWindowTitle(self.tr(name))
        self._alt_key = False
        self._ctrl_key = False

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_key = True
        if event.key() == QtCore.Qt.Key_Control:
            self._ctrl_key = True

        QtGui.QGraphicsView.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            self._alt_key = False
        if event.key() == QtCore.Qt.Key_Control:
            self._ctrl_key = False
        QtGui.QGraphicsView.keyReleaseEvent(self, event)

    def mousePressEvent(self,  event):

        self.pressed_item = self.itemAt(event.pos())
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        if self.pressed_item:
            self.pressed_item.setSelected(True)
        if event.button() == QtCore.Qt.LeftButton and self._alt_key:
            self.setDragMode(self.ScrollHandDrag)
        if event.button() == QtCore.Qt.LeftButton and self._ctrl_key:
            self.setDragMode(self.RubberBandDrag)
        super(GraphWidget, self).mousePressEvent(event)

    def clear_selection(self):
        print 'clear selection'
        for n in self.nodes:
            n.setSelected(False)

    def mouseMoveEvent(self, event):

        super(GraphWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        self.setDragMode(self.NoDrag)
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

    def wheelEvent(self, event):

        self.scale_view(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):

        # Shadow.
        scene_rect = self.sceneRect()
        # Fill.
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(self.kSceneBackground))
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

        AGraph.remove_edge(edge)
        self.edges.remove(edge)
        self.scene().removeItem(edge)

    def plot(self):
        for i in self.nodes:
            print i.name, i.isSelected()

    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if self.factor < 1 or self.factor > 5:
            return
        self.scale(scale_factor, scale_factor)

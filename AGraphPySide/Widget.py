from PySide import QtCore
from PySide import QtGui
import math
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


class RubberRect(QtGui.QGraphicsRectItem, Colors):
    def __init__(self, name):
        super(RubberRect, self).__init__()
        self.name = name
        self.setZValue(1)
        self.setPen(QtGui.QPen(self.kWhite, 1, QtCore.Qt.DotLine))


class GraphWidget(QtGui.QGraphicsView, Colors, AGraph):

    def __init__(self, name):
        QtGui.QGraphicsView.__init__(self)
        AGraph.__init__(self, name)
        self.pressed_item = None
        self.released_item = None
        self._isPanning = False
        self._mousePressed = False
        self.timerId = 0
        self.scale(1.5, 1.5)
        self.setViewportUpdateMode(self.FullViewportUpdate)
        self.setScene(SceneClass(self))
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.scene().setSceneRect(QtCore.QRect(0, 0, 2000, 2000))
        self.factor = 1
        self.scale(self.factor, self.factor)
        self.setWindowTitle(self.tr(name))
        self._alt_key = False
        self._ctrl_key = False
        self.rubber_rect = RubberRect('RubberRect')

        self.real_time_line = QtGui.QGraphicsLineItem(0, 0, 0, 0)
        self.real_time_line.name = 'RealTimeLine'
        self.real_time_line.setZValue(-1)
        self.real_time_line.setPen(QtGui.QPen(self.kWhite, 0.5, QtCore.Qt.DotLine))

        self.cursor_pressed_pos = None
        self.current_cursor_pose = None
        self._right_button = False
        self._is_rubber_band_selection = False
        self._draw_real_time_line = False
        self._update_items = False

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
        if self.pressed_item:
            if hasattr(self.pressed_item, 'object_type'):
                if self.pressed_item.object_type == AGObjectTypes.tPort:
                    self.pressed_item.parent.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
            else:
                self.pressed_item.setSelected(True)
        self.cursor_pressed_pos = self.mapToScene(event.pos())
        if self.pressed_item and event.button() == QtCore.Qt.LeftButton:
            if hasattr(self.pressed_item, 'object_type'):
                if self.pressed_item.object_type == AGObjectTypes.tPort:
                    self._draw_real_time_line = True
        if event.button() == QtCore.Qt.RightButton:
            self._right_button = True
        if all([event.button() == QtCore.Qt.LeftButton, self._alt_key]):
            self.setDragMode(self.ScrollHandDrag)
        if all([event.button() == QtCore.Qt.LeftButton, not self.pressed_item, not self._alt_key]):
            self._is_rubber_band_selection = True
        super(GraphWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.current_cursor_pose = self.mapToScene(event.pos())
        if self._draw_real_time_line:
            if self.real_time_line not in self.scene().items():
                self.scene().addItem(self.real_time_line)
            self.real_time_line.setLine(self.cursor_pressed_pos.x(),
                                        self.cursor_pressed_pos.y(),
                                        self.current_cursor_pose.x(),
                                        self.current_cursor_pose.y())
        if self._is_rubber_band_selection:
            if self.rubber_rect not in self.scene().items():
                self.scene().addItem(self.rubber_rect)
            if not self.rubber_rect.isVisible():
                self.rubber_rect.setVisible(True)
            r = QtCore.QRectF(self.cursor_pressed_pos.x(),
                              self.cursor_pressed_pos.y(),
                              self.current_cursor_pose.x()-self.cursor_pressed_pos.x(),
                              self.current_cursor_pose.y()-self.cursor_pressed_pos.y())
            self.rubber_rect.setRect(r.normalized())
        super(GraphWidget, self).mouseMoveEvent(event)

    def remove_item_by_name(self, name):

        [self.scene().removeItem(i) for i in self.scene().items() if hasattr(i, 'name') and i.name == name]

    def mouseReleaseEvent(self, event):

        self.setDragMode(self.NoDrag)
        for n in self.nodes:
            n.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        if event.button() == QtCore.Qt.RightButton:
            self._right_button = False
        if self._draw_real_time_line:
            self._draw_real_time_line = False
            if self.real_time_line in self.scene().items():
                self.remove_item_by_name('RealTimeLine')
        if self._is_rubber_band_selection:
            self._is_rubber_band_selection = False
            [i.setSelected(True) for i in self.rubber_rect.collidingItems()]
            self.remove_item_by_name(self.rubber_rect.name)
        if event.button() == QtCore.Qt.RightButton:
            self._right_button = False
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

    def add_node(self, node, x, y):

        AGraph.add_node(self, node, x, y)
        self.scene().addItem(node)
        node.setPos(QtCore.QPointF(x, y))

    def add_edge(self, src, dst):

        result = AGraph.add_edge(self, src, dst)
        if result:
            edge = Edge(src, dst)
            src.edge_list.append(edge)
            dst.edge_list.append(edge)
            self.scene().addItem(edge)
            self.edges.append(edge)
            return edge

    def remove_edge(self, edge):

        AGraph.remove_edge(self, edge)
        self.edges.remove(edge)
        self.scene().removeItem(edge)

    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        if self.factor < 1 or self.factor > 5:
            return
        self.scale(scale_factor, scale_factor)

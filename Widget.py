from PySide import QtCore
from PySide import QtGui
import math
from Node import Node
from Settings import Colors


class SceneClass(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(SceneClass, self).__init__(parent)
        self.Type = 'SCENE'
        self.setItemIndexMethod(self.NoIndex)
        self.setParent(parent)
        self.pressed_port = None

    def mouseMoveEvent(self, event):
        super(SceneClass, self).mouseMoveEvent(event)


class GraphWidget(QtGui.QGraphicsView, Colors):

    def __init__(self, name):
        QtGui.QGraphicsView.__init__(self)
        self.Type = 'VIEW'
        self.last_cursor_item = None
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

        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def keyPressEvent(self, event):

        key = event.key()

        if key == QtCore.Qt.Key_Plus:
            self.scale_view(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scale_view(1 / 1.2)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

    def mousePressEvent(self,  event):

        if event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(GraphWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.last_cursor_item = self.itemAt(event.pos())
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

    def scale_view(self, scale_factor):

        self.factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if self.factor < 0.3 or self.factor > 5:
            return

        self.scale(scale_factor, scale_factor)

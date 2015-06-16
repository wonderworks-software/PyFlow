from PySide import QtCore
from PySide import QtGui
import math


class GraphWidget(QtGui.QGraphicsView):

    def __init__(self):
        QtGui.QGraphicsView.__init__(self)

        self.last_cursor_item = None
        self._isPanning = False
        self._mousePressed = False
        self.timerId = 0
        self.setViewportUpdateMode(self.FullViewportUpdate)

        self.scene_widget = QtGui.QGraphicsScene(self)
        self.scene_widget.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene_widget.setSceneRect(-400, -400, 800, 800)
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(self.tr("Elastic Nodes"))

    def itemMoved(self):

        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def keyPressEvent(self, event):

        key = event.key()

        if key == QtCore.Qt.Key_Plus:
            self.scale_view(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scale_view(1 / 1.2)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, ConnectorItem):
                    item.setPos(-150 + QtCore.qrand() % 300, -150 + QtCore.qrand() % 300)
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

        nodes = [item for item in self.scene().items() if isinstance(item, ConnectorItem)]

        for node in nodes:
            node.calculate_forces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):

        self.scale_view(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):

        # Shadow.
        scene_rect = self.sceneRect()
        # Fill.
        gradient = QtGui.QColor(65, 65, 65)
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(scene_rect)

    def scale_view(self, scale_factor):

        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scale_factor, scale_factor)

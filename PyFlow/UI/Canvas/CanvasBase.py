from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

from PyFlow.UI.Canvas.UICommon import *


class CanvasBase(QGraphicsView):

    _manipulationMode = CanvasManipulationMode.NONE
    _mouseWheelZoomRate = 0.0005

    def __init__(self):
        super(CanvasBase, self).__init__()
        self.pressed_item = None
        self.released_item = None
        self.factor = 1
        self._minimum_scale = 0.2
        self._maximum_scale = 3.0
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # Antialias -- Change to Settings
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        ##
        self.setAcceptDrops(True)
        self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.setScene(self.createScene())

        self.scene().setSceneRect(QtCore.QRectF(0, 0, 10, 10))

        self.mousePressPose = QtCore.QPointF(0, 0)
        self.mousePos = QtCore.QPointF(0, 0)
        self._lastMousePos = QtCore.QPointF(0, 0)

        self.centerOn(QtCore.QPointF(self.sceneRect().width() / 2, self.sceneRect().height() / 2))

    def createScene(self):
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(QtCore.QRectF(0, 0, 10, 10))
        return scene

    def getItemsRect(self, cls=QGraphicsItem, bSelectedOnly=False, bVisibleOnly=True):
        rectangles = []
        for item in self.scene().items():
            if isinstance(item, cls):
                if bVisibleOnly and not item.isVisible():
                    continue
                if bSelectedOnly and not item.isSelected():
                    continue

                rect = item.sceneBoundingRect().toRect()
                rectangles.append(rect)

        result = QtCore.QRect()

        for r in rectangles:
            result |= r

        return result

    def jumpToItem(self, item):
        pass

    @property
    def manipulationMode(self):
        return self._manipulationMode

    @manipulationMode.setter
    def manipulationMode(self, value):
        self._manipulationMode = value
        if value == CanvasManipulationMode.NONE:
            pass
        elif value == CanvasManipulationMode.SELECT:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        elif value == CanvasManipulationMode.PAN:
            self.viewport().setCursor(QtCore.Qt.OpenHandCursor)
        elif value == CanvasManipulationMode.MOVE:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
        elif value == CanvasManipulationMode.ZOOM:
            self.viewport().setCursor(QtCore.Qt.SizeHorCursor)
        elif value == CanvasManipulationMode.COPY:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)

    def wheelEvent(self, event):
        (xfo, invRes) = self.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = (topLeft + bottomRight) * 0.5
        zoomFactor = 1.0 + event.delta() * self._mouseWheelZoomRate

        self.zoom(zoomFactor)

    def zoom(self, scale_factor):
        # TODO: Move to base class
        self.factor = self.transform().m22()
        futureScale = self.factor * scale_factor
        if futureScale <= self._minimum_scale:
            scale_factor = (self._minimum_scale) / self.factor
        if futureScale >= self._maximum_scale:
            scale_factor = (self._maximum_scale - 0.1) / self.factor
        self.scale(scale_factor, scale_factor)
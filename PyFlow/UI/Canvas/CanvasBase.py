from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Utils.stylesheet import editableStyleSheet


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

        self.centerOn(
            QtCore.QPointF(self.sceneRect().width() / 2, self.sceneRect().height() / 2)
        )

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

    def frameItems(self, items):
        rect = QtCore.QRect()
        for i in items:
            rect |= i.sceneBoundingRect().toRect()
        self.frameRect(rect)

    @property
    def manipulationMode(self):
        return self._manipulationMode

    @manipulationMode.setter
    def manipulationMode(self, value):
        self._manipulationMode = value
        if value == CanvasManipulationMode.NONE:
            self.viewport().setCursor(QtCore.Qt.ArrowCursor)
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
        zoomFactor = 1.0 + event.delta() * self._mouseWheelZoomRate

        self.zoom(zoomFactor)

    def zoom(self, scale_factor):
        self.factor = self.transform().m22()
        futureScale = self.factor * scale_factor
        if futureScale <= self._minimum_scale:
            scale_factor = self._minimum_scale / self.factor
        if futureScale >= self._maximum_scale:
            scale_factor = (self._maximum_scale - 0.1) / self.factor
        self.scale(scale_factor, scale_factor)

    def frameRect(self, rect):
        if rect is None:
            return
        windowRect = self.mapToScene(self.rect()).boundingRect()

        # pan to center of window
        delta = windowRect.center() - rect.center()
        delta *= self.currentViewScale()
        self.pan(delta)

        # zoom to fit content
        ws = windowRect.size()
        rect += QtCore.QMargins(40, 40, 40, 40)
        widthRef = ws.width()
        heightRef = ws.height()
        sx = widthRef / rect.width()
        sy = heightRef / rect.height()
        scale = sx if sy > sx else sy
        self.zoom(scale)

        return scale

    def zoomDelta(self, direction):
        if direction:
            self.zoom(1 + 0.1)
        else:
            self.zoom(1 - 0.1)

    def pan(self, delta):
        rect = self.sceneRect()
        scale = self.currentViewScale()
        x = -delta.x() / scale
        y = -delta.y() / scale
        rect.translate(x, y)
        self.setSceneRect(rect)
        self.update()

    def resetScale(self):
        self.resetMatrix()

    def viewMinimumScale(self):
        return self._minimum_scale

    def viewMaximumScale(self):
        return self._maximum_scale

    def currentViewScale(self):
        return self.transform().m22()

    def getLodValueFromScale(self, numLods=5, scale=1.0):
        lod = lerp(
            numLods,
            1,
            GetRangePct(self.viewMinimumScale(), self.viewMaximumScale(), scale),
        )
        return int(round(lod))

    def getLodValueFromCurrentScale(self, numLods=5):
        return self.getLodValueFromScale(numLods, self.currentViewScale())

    def getCanvasLodValueFromCurrentScale(self):
        return self.getLodValueFromScale(
            editableStyleSheet().LOD_Number[0], self.currentViewScale()
        )

    def drawBackground(self, painter, rect):
        super(CanvasBase, self).drawBackground(painter, rect)
        lod = self.getCanvasLodValueFromCurrentScale()
        self.boundingRect = rect

        painter.fillRect(rect, QtGui.QBrush(editableStyleSheet().CanvasBgColor))

        left = int(rect.left()) - (
            int(rect.left()) % editableStyleSheet().GridSizeFine[0]
        )
        top = int(rect.top()) - (int(rect.top()) % editableStyleSheet().GridSizeFine[0])

        if editableStyleSheet().DrawGrid[0] >= 1:
            if lod < editableStyleSheet().CanvasSwitch[0]:
                # Draw horizontal fine lines
                gridLines = []
                y = float(top)
                while y < float(rect.bottom()):
                    gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
                    y += editableStyleSheet().GridSizeFine[0]
                painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColor, 1))
                painter.drawLines(gridLines)

                # Draw vertical fine lines
                gridLines = []
                x = float(left)
                while x < float(rect.right()):
                    gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
                    x += editableStyleSheet().GridSizeFine[0]
                painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColor, 1))
                painter.drawLines(gridLines)

            # Draw thick grid
            left = int(rect.left()) - (
                int(rect.left()) % editableStyleSheet().GridSizeHuge[0]
            )
            top = int(rect.top()) - (
                int(rect.top()) % editableStyleSheet().GridSizeHuge[0]
            )

            # Draw vertical thick lines
            gridLines = []
            painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker, 1.5))
            x = left
            while x < rect.right():
                gridLines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
                x += editableStyleSheet().GridSizeHuge[0]
            painter.drawLines(gridLines)

            # Draw horizontal thick lines
            gridLines = []
            painter.setPen(QtGui.QPen(editableStyleSheet().CanvasGridColorDarker, 1.5))
            y = top
            while y < rect.bottom():
                gridLines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
                y += editableStyleSheet().GridSizeHuge[0]
            painter.drawLines(gridLines)

        if editableStyleSheet().DrawNumbers[0] >= 1:
            # draw numbers
            scale = self.currentViewScale()
            f = painter.font()
            f.setPointSize(6 / min(scale, 1))
            f.setFamily("Consolas")
            painter.setFont(f)
            y = float(top)

            while y < float(rect.bottom()):
                y += editableStyleSheet().GridSizeHuge[0]
                inty = int(y)
                if y > top + 30:
                    painter.setPen(
                        QtGui.QPen(
                            editableStyleSheet().CanvasGridColorDarker.lighter(300)
                        )
                    )
                    painter.drawText(rect.left(), y - 1.0, str(inty))

            x = float(left)
            while x < rect.right():
                x += editableStyleSheet().GridSizeHuge[0]
                intx = int(x)
                if x > left + 30:
                    painter.setPen(
                        QtGui.QPen(
                            editableStyleSheet().CanvasGridColorDarker.lighter(300)
                        )
                    )
                    painter.drawText(
                        x, rect.top() + painter.font().pointSize(), str(intx)
                    )

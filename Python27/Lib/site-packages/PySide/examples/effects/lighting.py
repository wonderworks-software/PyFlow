#!/usr/bin/env python


import math

from PySide import QtCore, QtGui


class Lighting(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(Lighting, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QtGui.QGraphicsScene()
        self.m_lightSource = None
        self.m_items = []

        self.setScene(self.m_scene)

        self.setupScene()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.animate)
        timer.setInterval(30)
        timer.start()

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setFrameStyle(QtGui.QFrame.NoFrame)

    def setupScene(self):
        self.m_scene.setSceneRect(-300, -200, 600, 460)

        linearGrad = QtGui.QLinearGradient(QtCore.QPointF(-100, -100),
                QtCore.QPointF(100, 100))
        linearGrad.setColorAt(0, QtGui.QColor(255, 255, 255))
        linearGrad.setColorAt(1, QtGui.QColor(192, 192, 255))
        self.setBackgroundBrush(linearGrad)

        radialGrad = QtGui.QRadialGradient(30, 30, 30)
        radialGrad.setColorAt(0, QtCore.Qt.yellow)
        radialGrad.setColorAt(0.2, QtCore.Qt.yellow)
        radialGrad.setColorAt(1, QtCore.Qt.transparent)

        pixmap = QtGui.QPixmap(60, 60)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, 60, 60)
        painter.end()

        self.m_lightSource = self.m_scene.addPixmap(pixmap)
        self.m_lightSource.setZValue(2)

        for i in range(-2, 3):
            for j in range(-2, 3):
                if (i + j) & 1:
                    item = QtGui.QGraphicsEllipseItem(0, 0, 50, 50)
                else:
                    item = QtGui.QGraphicsRectItem(0, 0, 50, 50)

                item.setPen(QtGui.QPen(QtCore.Qt.black, 1))
                item.setBrush(QtGui.QBrush(QtCore.Qt.white))

                effect = QtGui.QGraphicsDropShadowEffect(self)
                effect.setBlurRadius(8)
                item.setGraphicsEffect(effect)
                item.setZValue(1)
                item.setPos(i * 80, j * 80)
                self.m_scene.addItem(item)
                self.m_items.append(item)

    def animate(self):
        self.angle += (math.pi / 30)
        xs = 200 * math.sin(self.angle) - 40 + 25
        ys = 200 * math.cos(self.angle) - 40 + 25
        self.m_lightSource.setPos(xs, ys)

        for item in self.m_items:
            effect = item.graphicsEffect()

            delta = QtCore.QPointF(item.x() - xs, item.y() - ys)
            effect.setOffset(QtCore.QPointF(delta.toPoint() / 30))

            dd = math.hypot(delta.x(), delta.y())
            color = effect.color()
            color.setAlphaF(max(0.4, min(1 - dd / 200.0, 0.7)))
            effect.setColor(color)

        self.m_scene.update()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    lighting = Lighting()
    lighting.setWindowTitle("Lighting and Shadows")
    lighting.resize(640, 480)
    lighting.show()

    sys.exit(app.exec_())

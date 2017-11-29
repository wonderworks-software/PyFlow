#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2006-2006 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## Licensees holding a valid Qt License Agreement may use this file in
## accordance with the rights, responsibilities and obligations
## contained therein.  Please consult your licensing agreement or
## contact sales@trolltech.com if any conditions of this licensing
## agreement are not clear to you.
##
## Further information about Qt licensing is available at:
## http://www.trolltech.com/products/qt/licensing.html or by
## contacting info@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

import math

from PySide import QtCore, QtGui

import mice_rc


class Mouse(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    # Create the bounding rectangle once.
    adjust = 0.5
    BoundingRect = QtCore.QRectF(-20 - adjust, -22 - adjust, 40 + adjust,
            83 + adjust)

    def __init__(self):
        super(Mouse, self).__init__()

        self.angle = 0.0
        self.speed = 0.0
        self.mouseEyeDirection = 0.0
        self.color = QtGui.QColor(QtCore.qrand() % 256, QtCore.qrand() % 256,
                QtCore.qrand() % 256)

        self.rotate(QtCore.qrand() % (360 * 16))

        # In the C++ version of this example, this class is also derived from
        # QObject in order to receive timer events.  PyQt does not support
        # deriving from more than one wrapped class so we just create an
        # explicit timer instead.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000 / 33)

    @staticmethod
    def normalizeAngle(angle):
        while angle < 0:
            angle += Mouse.TwoPi
        while angle > Mouse.TwoPi:
            angle -= Mouse.TwoPi
        return angle

    def boundingRect(self):
        return Mouse.BoundingRect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(-10, -20, 20, 40)
        return path;

    def paint(self, painter, option, widget):
        # Body.
        painter.setBrush(self.color)
        painter.drawEllipse(-10, -20, 20, 40)

        # Eyes.
        painter.setBrush(QtCore.Qt.white)
        painter.drawEllipse(-10, -17, 8, 8)
        painter.drawEllipse(2, -17, 8, 8)

        # Nose.
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(QtCore.QRectF(-2, -22, 4, 4))

        # Pupils.
        painter.drawEllipse(QtCore.QRectF(-8.0 + self.mouseEyeDirection, -17, 4, 4))
        painter.drawEllipse(QtCore.QRectF(4.0 + self.mouseEyeDirection, -17, 4, 4))

        # Ears.
        if self.scene().collidingItems(self):
            painter.setBrush(QtCore.Qt.red)
        else:
            painter.setBrush(QtCore.Qt.darkYellow)

        painter.drawEllipse(-17, -12, 16, 16)
        painter.drawEllipse(1, -12, 16, 16)

        # Tail.
        path = QtGui.QPainterPath(QtCore.QPointF(0, 20))
        path.cubicTo(-5, 22, -5, 22, 0, 25)
        path.cubicTo(5, 27, 5, 32, 0, 30)
        path.cubicTo(-5, 32, -5, 42, 0, 35)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path)

    def timerEvent(self):
        # Don't move too far away.
        lineToCenter = QtCore.QLineF(QtCore.QPointF(0, 0), self.mapFromScene(0, 0))
        if lineToCenter.length() > 150:
            angleToCenter = math.acos(lineToCenter.dx() / lineToCenter.length())
            if lineToCenter.dy() < 0:
                angleToCenter = Mouse.TwoPi - angleToCenter;
            angleToCenter = Mouse.normalizeAngle((Mouse.Pi - angleToCenter) + Mouse.Pi / 2)

            if angleToCenter < Mouse.Pi and angleToCenter > Mouse.Pi / 4:
                # Rotate left.
                self.angle += [-0.25, 0.25][self.angle < -Mouse.Pi / 2]
            elif angleToCenter >= Mouse.Pi and angleToCenter < (Mouse.Pi + Mouse.Pi / 2 + Mouse.Pi / 4):
                # Rotate right.
                self.angle += [-0.25, 0.25][self.angle < Mouse.Pi / 2]
        elif math.sin(self.angle) < 0:
            self.angle += 0.25
        elif math.sin(self.angle) > 0:
            self.angle -= 0.25

        # Try not to crash with any other mice.
        dangerMice = self.scene().items(QtGui.QPolygonF([self.mapToScene(0, 0),
                                                         self.mapToScene(-30, -50),
                                                         self.mapToScene(30, -50)]))

        for item in dangerMice:
            if item is self:
                continue
        
            lineToMouse = QtCore.QLineF(QtCore.QPointF(0, 0), self.mapFromItem(item, 0, 0))
            angleToMouse = math.acos(lineToMouse.dx() / lineToMouse.length())
            if lineToMouse.dy() < 0:
                angleToMouse = Mouse.TwoPi - angleToMouse
            angleToMouse = Mouse.normalizeAngle((Mouse.Pi - angleToMouse) + Mouse.Pi / 2)

            if angleToMouse >= 0 and angleToMouse < Mouse.Pi / 2:
                # Rotate right.
                self.angle += 0.5
            elif angleToMouse <= Mouse.TwoPi and angleToMouse > (Mouse.TwoPi - Mouse.Pi / 2):
                # Rotate left.
                self.angle -= 0.5

        # Add some random movement.
        if len(dangerMice) > 1 and (QtCore.qrand() % 10) == 0:
            if QtCore.qrand() % 1:
                self.angle += (QtCore.qrand() % 100) / 500.0
            else:
                self.angle -= (QtCore.qrand() % 100) / 500.0

        self.speed += (-50 + QtCore.qrand() % 100) / 100.0

        dx = math.sin(self.angle) * 10
        self.mouseEyeDirection = [dx / 5, 0.0][QtCore.qAbs(dx / 5) < 1]

        self.rotate(dx)
        self.setPos(self.mapToParent(0, -(3 + math.sin(self.speed) * 3)))


if __name__ == '__main__':

    import sys

    MouseCount = 7

    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    scene = QtGui.QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

    for i in range(MouseCount):
        mouse = Mouse()
        mouse.setPos(math.sin((i * 6.28) / MouseCount) * 200,
                     math.cos((i * 6.28) / MouseCount) * 200)
        scene.addItem(mouse)

    view = QtGui.QGraphicsView(scene)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(':/images/cheese.jpg')))
    view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Colliding Mice")
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())

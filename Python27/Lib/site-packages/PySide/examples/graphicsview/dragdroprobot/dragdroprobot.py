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

from PySide import QtCore, QtGui

import dragdroprobot_rc


class ColorItem(QtGui.QGraphicsItem):
    n = 0

    def __init__(self):
        super(ColorItem, self).__init__()

        self.color = QtGui.QColor(QtCore.qrand() % 256, QtCore.qrand() % 256,
                QtCore.qrand() % 256)

        self.setToolTip(
            "QColor(%d, %d, %d)\nClick and drag this color onto the robot!" % 
              (self.color.red(), self.color.green(), self.color.blue())
        )
        self.setCursor(QtCore.Qt.OpenHandCursor)
    
    def boundingRect(self):
        return QtCore.QRectF(-15.5, -15.5, 34, 34)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-12, -12, 30, 30)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(-15, -15, 30, 30)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if QtCore.QLineF(QtCore.QPointF(event.screenPos()), QtCore.QPointF(event.buttonDownScreenPos(QtCore.Qt.LeftButton))).length() < QtGui.QApplication.startDragDistance():
            return

        drag = QtGui.QDrag(event.widget())
        mime = QtCore.QMimeData()
        drag.setMimeData(mime)

        ColorItem.n += 1
        if ColorItem.n > 2 and QtCore.qrand() % 3 == 0:
            image = QtGui.QImage(':/images/head.png')
            mime.setImageData(image)
            drag.setPixmap(QtGui.QPixmap.fromImage(image).scaled(30,40))
            drag.setHotSpot(QtCore.QPoint(15, 30))
        else:
            mime.setColorData(self.color)
            mime.setText("#%02x%02x%02x" % (self.color.red(), self.color.green(), self.color.blue()))

            pixmap = QtGui.QPixmap(34, 34)
            pixmap.fill(QtCore.Qt.white)

            painter = QtGui.QPainter(pixmap)
            painter.translate(15, 15)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self.paint(painter, None, None)
            painter.end()

            pixmap.setMask(pixmap.createHeuristicMask())

            drag.setPixmap(pixmap)
            drag.setHotSpot(QtCore.QPoint(15, 20))

        drag.exec_()
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)


class RobotPart(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(RobotPart, self).__init__(parent)

        self.color = QtGui.QColor(QtCore.Qt.lightGray)
        self.pixmap = None
        self.dragOver = False

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasColor() or \
          (isinstance(self, RobotHead) and event.mimeData().hasImage()):
            event.setAccepted(True)
            self.dragOver = True
            self.update()
        else:
            event.setAccepted(False)

    def dragLeaveEvent(self, event):
        self.dragOver = False
        self.update()
 
    def dropEvent(self, event):
        self.dragOver = False
        if event.mimeData().hasColor():
            self.color = QtGui.QColor(event.mimeData().colorData())
        elif event.mimeData().hasImage():
            self.pixmap = QtGui.QPixmap(event.mimeData().imageData())

        self.update()


class RobotHead(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-15, -50, 30, 50)

    def paint(self, painter, option, widget=None):
        if not self.pixmap:
            painter.setBrush(self.dragOver and self.color.lighter(130) 
                                            or self.color)
            painter.drawRoundedRect(-10, -30, 20, 30, 25, 25,
                    QtCore.Qt.RelativeSize)
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(-7, -3 - 20, 7, 7)
            painter.drawEllipse(0, -3 - 20, 7, 7)
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(-5, -1 - 20, 2, 2)
            painter.drawEllipse(2, -1 - 20, 2, 2)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawArc(-6, -2 - 20, 12, 15, 190 * 16, 160 * 16)
        else:
            painter.scale(.2272, .2824)
            painter.drawPixmap(QtCore.QPointF(-15*4.4, -50*3.54), self.pixmap)


class RobotTorso(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-30, -20, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.dragOver and self.color.lighter(130) 
                                        or self.color)
        painter.drawRoundedRect(-20, -20, 40, 60, 25, 25,
                QtCore.Qt.RelativeSize)
        painter.drawEllipse(-25, -20, 20, 20)
        painter.drawEllipse(5, -20, 20, 20)
        painter.drawEllipse(-20, 22, 20, 20)
        painter.drawEllipse(0, 22, 20, 20)


class RobotLimb(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-5, -5, 40, 10)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.dragOver and self.color.lighter(130) or self.color)
        painter.drawRoundedRect(self.boundingRect(), 50, 50,
                QtCore.Qt.RelativeSize)
        painter.drawEllipse(-5, -5, 10, 10)


class Robot(RobotPart):
    def __init__(self):
        super(Robot, self).__init__()

        self.torsoItem         = RobotTorso(self)
        self.headItem          = RobotHead(self.torsoItem)
        self.upperLeftArmItem  = RobotLimb(self.torsoItem)
        self.lowerLeftArmItem  = RobotLimb(self.upperLeftArmItem)
        self.upperRightArmItem = RobotLimb(self.torsoItem)
        self.lowerRightArmItem = RobotLimb(self.upperRightArmItem)
        self.upperRightLegItem = RobotLimb(self.torsoItem)
        self.lowerRightLegItem = RobotLimb(self.upperRightLegItem)
        self.upperLeftLegItem  = RobotLimb(self.torsoItem)
        self.lowerLeftLegItem  = RobotLimb(self.upperLeftLegItem)

        self.timeline = QtCore.QTimeLine()
        settings = [
        #             item               position    rotation at
        #                                 x    y    time 0  /  1
            ( self.headItem,              0,  -18,      20,   -20 ),
            ( self.upperLeftArmItem,    -15,  -10,     190,   180 ),
            ( self.lowerLeftArmItem,     30,    0,      50,    10 ),
            ( self.upperRightArmItem,    15,  -10,     300,   310 ),
            ( self.lowerRightArmItem,    30,    0,       0,   -70 ),
            ( self.upperRightLegItem,    10,   32,      40,   120 ),
            ( self.lowerRightLegItem,    30,    0,      10,    50 ),
            ( self.upperLeftLegItem,    -10,   32,     150,    80 ),
            ( self.lowerLeftLegItem,     30,    0,      70,    10 ),
            ( self.torsoItem,             0,    0,       5,   -20 )
        ]
        self.animations = []
        for item, pos_x, pos_y, rotation1, rotation2 in settings: 
            item.setPos(pos_x,pos_y)
            animation = QtGui.QGraphicsItemAnimation()
            animation.setItem(item)
            animation.setTimeLine(self.timeline)
            animation.setRotationAt(0, rotation1)
            animation.setRotationAt(1, rotation2)
            self.animations.append(animation)
        self.animations[0].setScaleAt(1, 1.1, 1.1)
    
        self.timeline.setUpdateInterval(1000 / 25)
        self.timeline.setCurveShape(QtCore.QTimeLine.SineCurve)
        self.timeline.setLoopCount(0)
        self.timeline.setDuration(2000)
        self.timeline.start()

    def boundingRect(self):
        return QtCore.QRectF()

    def paint(self, painter, option, widget=None):
        pass


if __name__== '__main__':

    import sys
    import math

    app = QtGui.QApplication(sys.argv)

    QtCore.qsrand(QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.currentTime()))

    scene = QtGui.QGraphicsScene(-200, -200, 400, 400)

    for i in range(10):
        item = ColorItem()
        angle = i*6.28 / 10.0
        item.setPos(math.sin(angle)*150, math.cos(angle)*150)
        scene.addItem(item)

    robot = Robot()
    robot.scale(1.2, 1.2)
    robot.setPos(0, -20)
    scene.addItem(robot)

    view = QtGui.QGraphicsView(scene)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.setBackgroundBrush(QtGui.QColor(230, 200, 167))
    view.setWindowTitle("Drag and Drop Robot")
    view.show()

    sys.exit(app.exec_())

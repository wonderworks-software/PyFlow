#!/usr/bin/env python

# PyQt tutorial 11


import sys
import math
from PySide import QtCore, QtGui


class LCDRange(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        lcd = QtGui.QLCDNumber(2)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)

    def setRange(self, minValue, maxValue):
        if minValue < 0 or maxValue > 99 or minValue > maxValue:
            QtCore.qWarning("LCDRange::setRange(%d, %d)\n"
                    "\tRange must be 0..99\n"
                    "\tand minValue must not be greater than maxValue" % (minValue, maxValue))
            return

        self.slider.setRange(minValue, maxValue)


class CannonField(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.currentAngle = 45
        self.currentForce = 0
        self.timerCount = 0
        self.autoShootTimer = QtCore.QTimer(self)
        self.connect(self.autoShootTimer, QtCore.SIGNAL("timeout()"),
                     self.moveShot)
        self.shootAngle = 0
        self.shootForce = 0
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)

    def angle(self):
        return self.currentAngle

    def setAngle(self, angle):
        if angle < 5:
            angle = 5
        if angle > 70:
            angle = 70;
        if self.currentAngle == angle:
            return
        self.currentAngle = angle
        self.update()
        self.emit(QtCore.SIGNAL("angleChanged(int)"), self.currentAngle)

    def force(self):
        return self.currentForce

    def setForce(self, force):
        if force < 0:
            force = 0
        if self.currentForce == force:
            return
        self.currentForce = force;
        self.emit(QtCore.SIGNAL("forceChanged(int)"), self.currentForce)

    def shoot(self):
        if self.autoShootTimer.isActive():
            return
        self.timerCount = 0
        self.shootAngle = self.currentAngle
        self.shootForce = self.currentForce
        self.autoShootTimer.start(5)

    def moveShot(self):
        region = QtGui.QRegion(self.shotRect())
        self.timerCount += 1

        shotR = self.shotRect()

        if shotR.x() > self.width() or shotR.y() > self.height():
            self.autoShootTimer.stop()
        else:
            region = region.united(QtGui.QRegion(shotR))

        self.update(region)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        self.paintCannon(painter)
        if self.autoShootTimer.isActive():
            self.paintShot(painter)

    def paintShot(self, painter):
        painter.setPen(QtCore.Qt.NoPen);
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

    barrelRect = QtCore.QRect(33, -4, 15, 8)

    def paintCannon(self, painter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.blue)

        painter.save()
        painter.translate(0, self.height())
        painter.drawPie(QtCore.QRect(-35, -35, 70, 70), 0, 90 * 16)
        painter.rotate(-self.currentAngle)
        painter.drawRect(CannonField.barrelRect)
        painter.restore()

    def cannonRect(self):
        result = QtCore.QRect(0, 0, 50, 50)
        result.moveBottomLeft(self.rect().bottomLect())
        return result

    def shotRect(self):
        gravity = 4.0

        time = self.timerCount / 40.0
        velocity = self.shootForce
        radians = self.shootAngle * 3.14159265 / 180

        velx = velocity * math.cos(radians)
        vely = velocity * math.sin(radians)
        x0 = (CannonField.barrelRect.right() + 5) * math.cos(radians)
        y0 = (CannonField.barrelRect.right() + 5) * math.sin(radians)
        x = x0 + velx * time
        y = y0 + vely * time - 0.5 * gravity * time * time

        result = QtCore.QRect(0, 0, 6, 6)
        result.moveCenter(QtCore.QPoint(QtCore.qRound(x), self.height() - 1 - QtCore.qRound(y)))
        return result


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        quit = QtGui.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        angle = LCDRange()
        angle.setRange(5, 70)

        force = LCDRange()
        force.setRange(10, 50)

        cannonField = CannonField()

        self.connect(angle, QtCore.SIGNAL("valueChanged(int)"),
                     cannonField.setAngle)
        self.connect(cannonField, QtCore.SIGNAL("angleChanged(int)"),
                     angle.setValue)

        self.connect(force, QtCore.SIGNAL("valueChanged(int)"),
                     cannonField.setForce)
        self.connect(cannonField, QtCore.SIGNAL("forceChanged(int)"),
                     force.setValue)

        shoot = QtGui.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(shoot, QtCore.SIGNAL("clicked()"), cannonField.shoot)

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(shoot)
        topLayout.addStretch(1)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(angle)
        leftLayout.addWidget(force)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addWidget(cannonField, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        angle.setValue(60)
        force.setValue(25)
        angle.setFocus()


app = QtGui.QApplication(sys.argv)
widget = MyWidget()
widget.setGeometry(100, 100, 500, 355)
widget.show()
sys.exit(app.exec_())

#!/usr/bin/env python

# PyQt tutorial 14


import sys
import math
import random
from PySide import QtCore, QtGui


class LCDRange(QtGui.QWidget):
    def __init__(self, text=None, parent=None):
        if isinstance(text, QtGui.QWidget):
            parent = text
            text = None

        QtGui.QWidget.__init__(self, parent)

        self.init()

        if text:
            self.setText(text)

    def init(self):
        lcd = QtGui.QLCDNumber(2)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 99)
        self.slider.setValue(0)
        self.label = QtGui.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     lcd, QtCore.SLOT("display(int)"))
        self.connect(self.slider, QtCore.SIGNAL("valueChanged(int)"),
                     self, QtCore.SIGNAL("valueChanged(int)"))

        layout = QtGui.QVBoxLayout()
        layout.addWidget(lcd)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFocusProxy(self.slider)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)

    def text(self):
        return self.label.text()

    def setRange(self, minValue, maxValue):
        if minValue < 0 or maxValue > 99 or minValue > maxValue:
            QtCore.qWarning("LCDRange::setRange(%d, %d)\n"
                    "\tRange must be 0..99\n"
                    "\tand minValue must not be greater than maxValue" % (minValue, maxValue))
            return

        self.slider.setRange(minValue, maxValue)

    def setText(self, text):
        self.label.setText(text)


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
        self.target = QtCore.QPoint(0, 0)
        self.gameEnded = False
        self.barrelPressed = False
        self.setPalette(QtGui.QPalette(QtGui.QColor(250, 250, 200)))
        self.setAutoFillBackground(True)
        self.newTarget()

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
        if self.isShooting():
            return
        self.timerCount = 0
        self.shootAngle = self.currentAngle
        self.shootForce = self.currentForce
        self.autoShootTimer.start(5)
        self.emit(QtCore.SIGNAL("canShoot(bool)"), False)

    firstTime = True

    def newTarget(self):
        if CannonField.firstTime:
            CannonField.firstTime = False
            midnight = QtCore.QTime(0, 0, 0)
            random.seed(midnight.secsTo(QtCore.QTime.currentTime()))

        self.target = QtCore.QPoint(200 + random.randint(0, 190 - 1), 10 + random.randint(0, 255 - 1))
        self.update()

    def setGameOver(self):
        if self.gameEnded:
            return
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = True
        self.update()

    def restartGame(self):
        if self.isShooting():
            self.autoShootTimer.stop()
        self.gameEnded = False
        self.update()
        self.emit(QtCore.SIGNAL("canShoot(bool)"), True)

    def moveShot(self):
        region = QtGui.QRegion(self.shotRect())
        self.timerCount += 1

        shotR = self.shotRect()

        if shotR.intersects(self.targetRect()):
            self.autoShootTimer.stop()
            self.emit(QtCore.SIGNAL("hit()"))
            self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        elif shotR.x() > self.width() or shotR.y() > self.height() or shotR.intersects(self.barrierRect()):
            self.autoShootTimer.stop()
            self.emit(QtCore.SIGNAL("missed()"))
            self.emit(QtCore.SIGNAL("canShoot(bool)"), True)
        else:
            region = region.united(QtGui.QRegion(shotR))

        self.update(region)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return
        if self.barrelHit(event.pos()):
            self.barrelPressed = True

    def mouseMoveEvent(self, event):
        if not self.barrelPressed:
            return
        pos = event.pos()
        if pos.x() <= 0:
            pos.setX(1)
        if pos.y() >= self.height():
            pos.setY(self.height() - 1)
        rad = math.atan((float(self.rect().bottom()) - pos.y()) / pos.x())
        self.setAngle(QtCore.qRound(rad * 180 / 3.14159265))

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.barrelPressed = False;

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        if self.gameEnded:
            painter.setPen(QtCore.Qt.black)
            painter.setFont(QtGui.QFont("Courier", 48, QtGui.QFont.Bold))
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Game Over")

        self.paintCannon(painter)
        self.paintBarrier(painter)
        if self.isShooting():
            self.paintShot(painter)
        if not self.gameEnded:
            self.paintTarget(painter)

    def paintShot(self, painter):
        painter.setPen(QtCore.Qt.NoPen);
        painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.shotRect())

    def paintTarget(self, painter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(self.targetRect())

    def paintBarrier(self, painter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.yellow)
        painter.drawRect(self.barrierRect())

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

    def targetRect(self):
        result = QtCore.QRect(0, 0, 20, 10)
        result.moveCenter(QtCore.QPoint(self.target.x(), self.height() - 1 - self.target.y()))
        return result

    def barrierRect(self):
        return QtCore.QRect(145, self.height() - 100, 15, 99)

    def barrelHit(self, pos):
        matrix = QtGui.QMatrix()
        matrix.translate(0, self.height())
        matrix.rotate(-self.currentAngle)
        matrix, invertible = matrix.inverted()
        return self.barrelRect.contains(matrix.map(pos))

    def gameOver(self):
        return self.gameEnded

    def isShooting(self):
        return self.autoShootTimer.isActive()

    def sizeHint(self):
        return QtCore.QSize(400, 300)


class GameBoard(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        quit = QtGui.QPushButton("&Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))

        angle = LCDRange("ANGLE")
        angle.setRange(5, 70)

        force = LCDRange("FORCE")
        force.setRange(10, 50)

        cannonBox = QtGui.QFrame()
        cannonBox.setFrameStyle(QtGui.QFrame.WinPanel | QtGui.QFrame.Sunken)

        self.cannonField = CannonField()

        self.connect(angle, QtCore.SIGNAL("valueChanged(int)"),
                     self.cannonField.setAngle)
        self.connect(self.cannonField, QtCore.SIGNAL("angleChanged(int)"),
                     angle.setValue)

        self.connect(force, QtCore.SIGNAL("valueChanged(int)"),
                     self.cannonField.setForce)
        self.connect(self.cannonField, QtCore.SIGNAL("forceChanged(int)"),
                     force.setValue)

        self.connect(self.cannonField, QtCore.SIGNAL("hit()"), self.hit)
        self.connect(self.cannonField, QtCore.SIGNAL("missed()"), self.missed)

        shoot = QtGui.QPushButton("&Shoot")
        shoot.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(shoot, QtCore.SIGNAL("clicked()"), self.fire)
        self.connect(self.cannonField, QtCore.SIGNAL("canShoot(bool)"),
                     shoot, QtCore.SLOT("setEnabled(bool)"))

        restart = QtGui.QPushButton("&New Game")
        restart.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))

        self.connect(restart, QtCore.SIGNAL("clicked()"), self.newGame)

        self.hits = QtGui.QLCDNumber(2)
        self.shotsLeft = QtGui.QLCDNumber(2)
        hitsLabel = QtGui.QLabel("HITS")
        shotsLeftLabel = QtGui.QLabel("SHOTS LEFT")

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter),
                        self, self.fire)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return),
                        self, self.fire)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Q),
                        self, QtCore.SLOT("close()"))

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(shoot)
        topLayout.addWidget(self.hits)
        topLayout.addWidget(hitsLabel)
        topLayout.addWidget(self.shotsLeft)
        topLayout.addWidget(shotsLeftLabel)
        topLayout.addStretch(1)
        topLayout.addWidget(restart)

        leftLayout = QtGui.QVBoxLayout()
        leftLayout.addWidget(angle)
        leftLayout.addWidget(force)

        cannonLayout = QtGui.QVBoxLayout()
        cannonLayout.addWidget(self.cannonField)
        cannonBox.setLayout(cannonLayout)

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(quit, 0, 0)
        gridLayout.addLayout(topLayout, 0, 1)
        gridLayout.addLayout(leftLayout, 1, 0)
        gridLayout.addWidget(cannonBox, 1, 1, 2, 1)
        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

        angle.setValue(60)
        force.setValue(25)
        angle.setFocus()

        self.newGame()

    def fire(self):
        if self.cannonField.gameOver() or self.cannonField.isShooting():
            return
        self.shotsLeft.display(self.shotsLeft.intValue() - 1)
        self.cannonField.shoot()

    def hit(self):
        self.hits.display(self.hits.intValue() + 1)
        if self.shotsLeft.intValue() == 0:
            self.cannonField.setGameOver()
        else:
            self.cannonField.newTarget()

    def missed(self):
        if self.shotsLeft.intValue() == 0:
            self.cannonField.setGameOver()

    def newGame(self):
        self.shotsLeft.display(15)
        self.hits.display(0)
        self.cannonField.restartGame()
        self.cannonField.newTarget()


app = QtGui.QApplication(sys.argv)
board = GameBoard()
board.setGeometry(100, 100, 500, 355)
board.show()
sys.exit(app.exec_())

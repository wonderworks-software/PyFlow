"""
/*
 * This file is part of PySide: Python for Qt
 *
 * Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * version 2.1 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 *
 */
"""


from PySide import QtGui, QtCore

class KineticScroll(QtCore.QObject):
    MAX_SPEED = 2000

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self._area = parent
        self._animation = None
        self._animationSpeed = 0
        self._animationITime = QtCore.QTime()
        self._animationAccel = 0
        self._accelConstant = 0.3
        self._value = self._lastValue = -1
        self._time = self._lastTime = QtCore.QTime.currentTime()

    def mouseUp(self, value):
        if self._lastValue < 0 or self._animation != None:
            return

        t = QtCore.QTime.currentTime()
        dv = value - self._lastValue
        dt = self._lastTime.msecsTo(t) / 1000.0

        if dt == 0:
            return

        self.kineticStart(dv/dt)
        self.mouseCancel()

    def mouseDown(self, value):
        r = True
        if self._animation:
            self._animation.stop()
            self._animation.deleteLater()
            self._animation = None
            r = False

        self._lastValue = value
        self._value = value
        self._lastTime = QtCore.QTime.currentTime()
        self._time = QtCore.QTime.currentTime()

        return r


    def mouseMove(self, value):
        if self._lastValue < 0:
            return

        dv = value - self._value
        t = QtCore.QTime.currentTime()

        self._lastValue = self._value
        self._lastTime = self._time
        self._value = value
        self._time = t

        self.emit(QtCore.SIGNAL("signalMoveOffset(int)"), dv)

    def mouseCancel(self):
        self._value = self._lastValue = -1

    def kineticStop(self):
        if self._animation:
            self._animation.stop()
            self._animation.deleteLater()

        self._animation = None

    def kineticStart(self, speed):
        self._animationSpeed = max(min(speed, self.MAX_SPEED), -self.MAX_SPEED)
        self._animationITime = QtCore.QTime.currentTime()
        self._animationAccel = -self._animationSpeed * self._accelConstant

        self._animation = QtCore.QTimer(self)
        self.connect(self._animation, QtCore.SIGNAL("timeout()"), self.animator)
        self._animation.start(30)

    def animator(self):
        now = QtCore.QTime.currentTime()
        dt = self._animationITime.msecsTo(now) / 1000.0
        speed = self._animationSpeed + self._animationAccel * dt
        value = self._animationSpeed * dt + self._animationAccel * dt * dt / 2

        if self._animationAccel * speed > 0:
            self.emit(QtCore.SIGNAL("signalMoveOffset(int)"), 0)
            #self._area.kineticMove(0)
            self.kineticStop()
        else:
            self.emit(QtCore.SIGNAL("signalMoveOffset(int)"), round(value))
            #self._area.kineticMove(round(value))
            self._animationSpeed = speed
            self._animationITime = now


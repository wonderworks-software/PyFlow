"""@file PinPainter.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QStyle
from Settings import *


## Determines how to paint a pin
class PinPainter(object):

    _execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)

    @staticmethod
    def asValuePin(pin, painter, option, widget):
        background_rect = QtCore.QRectF(0, 0, pin.width, pin.width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), pin.width / 2.5)
        if not pin._rawPin._connected:
            linearGrad.setColorAt(0, pin.color().darker(280))
            linearGrad.setColorAt(0.5, pin.color().darker(280))
            linearGrad.setColorAt(0.65, pin.color().lighter(130))
            linearGrad.setColorAt(1, pin.color().lighter(70))
        else:
            linearGrad.setColorAt(0, pin.color())
            linearGrad.setColorAt(1, pin.color())

        if pin.hovered:
            linearGrad.setColorAt(1, pin.color().lighter(200))

        painter.setBrush(QtGui.QBrush(linearGrad))
        rect = background_rect.setX(background_rect.x())
        painter.drawEllipse(background_rect)

    @staticmethod
    def asExecPin(pin, painter, option, widget):
        painter.setPen(PinPainter._execPen)
        if pin._rawPin._connected:
            painter.setBrush(QtGui.QBrush(pin.color()))
        else:
            painter.setBrush(QtCore.Qt.NoBrush)
        arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                QtCore.QPointF(pin.width / 2.0, 0.0),
                                QtCore.QPointF(pin.width, pin.height / 2.0),
                                QtCore.QPointF(pin.width / 2.0, pin.height),
                                QtCore.QPointF(0, pin.height)])
        painter.drawPolygon(arrow)

    @staticmethod
    def asArrayPin(pin, painter, option, widget):
        painter.setBrush(QtGui.QBrush(pin.color()))

        size = 3

        w = pin.width / size
        h = pin.height / size

        for row in range(size):
            for column in range(size):
                x = row * w
                y = column * h
                painter.drawRect(x, y, w, h)

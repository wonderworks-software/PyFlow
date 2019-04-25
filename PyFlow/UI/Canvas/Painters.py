"""@file NodePainter.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QStyle

from PyFlow.UI.Utils.Settings import *


# Determines how to paint the node
class NodePainter(object):

    @staticmethod
    def default(node, painter, option, widget):
        # use 3 levels of detail
        lod = node.canvasRef().getLodValueFromCurrentScale(3)

        color = node.color
        color.setAlpha(230)
        if node.isSelected():
            color = color.lighter(150)
        if node.isTemp:
            color = color.lighter(50)
            color.setAlpha(50)

        br = QtGui.QBrush(color)
        painter.setBrush(br)

        pen = QtGui.QPen(QtCore.Qt.black, 0.75)
        painter.setPen(QtCore.Qt.NoPen)
        r = QtCore.QRectF(node.boundingRect())
        r.setWidth(r.width() - pen.width())
        r.setHeight(r.height() - pen.width())
        r.setX(pen.width())
        r.setY(r.y() + pen.width())
        painter.drawRoundedRect(r, node.sizes[4], node.sizes[5])

        br = QtGui.QBrush()
        painter.setBrush(br)
        if node.label().isVisible():
            headColor = node.headColor
            if node.isTemp:
                headColor = headColor.lighter(50)
                headColor.setAlpha(50)
            lr = QtCore.QRectF(r)
            lr.setHeight(node.label().h)
            b = QtGui.QLinearGradient(0, 0, lr.width(), 0)
            b.setColorAt(0, headColor.lighter(60))
            b.setColorAt(0.5, headColor)
            b.setColorAt(1, headColor.darker(50))
            path = QtGui.QPainterPath()
            path.setFillRule(QtCore.Qt.WindingFill)
            path.addRoundedRect(lr, node.sizes[4], node.sizes[5])
            lr.setY(lr.y() + node.sizes[5])
            path.addRect(lr)
            painter.fillPath(path, b)

        if option.state & QStyle.State_Selected:
            # pen.setColor(Colors.Yellow)
            pen.setColor(
                node.canvasRef().window().styleSheetEditor.style.MainColor)
            pen.setStyle(node.opt_pen_selected_type)
            pen.setWidth(pen.width() * 1.5)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawRoundedRect(r, node.sizes[4], node.sizes[5])

    @staticmethod
    def asVariableGetter(node, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = node.color
        if node.isSelected():
            color = color.lighter(150)

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            # pen.setColor(Colors.Yellow)
            pen.setColor(
                node.canvasRef().window().styleSheetEditor.style.MainColor)
            pen.setStyle(node.opt_pen_selected_type)
        painter.setPen(pen)
        painter.drawRoundedRect(node.boundingRect(), 7, 7)
        painter.setFont(node.label().opt_font)
        # pen.setColor(QtGui.QColor(*node.var.widget.color))
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 0.5))
        textRect = node.boundingRect()
        textRect.setWidth(textRect.width() - 10)
        painter.drawText(textRect, QtCore.Qt.AlignCenter |
                         QtCore.Qt.AlignVCenter, node.displayName)

    @staticmethod
    def asRerouteNode(node, painter, option, widget):
        color = node.color
        color.setAlpha(255)
        # if node.isSelected():
        color = color.lighter(100)
        if node.isTemp:
            color = color.lighter(50)
            color.setAlpha(50)
        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)

        pen = QtGui.QPen(QtCore.Qt.black, 0.75)
        width = pen.width()
        if option.state & QStyle.State_Selected:
            # pen.setColor(Colors.Yellow)
            pen.setColor(
                node.canvasRef().window().styleSheetEditor.style.MainColor)
            pen.setStyle(node.opt_pen_selected_type)
            pen.setWidth(width * 1.5)
        painter.setPen(pen)
        painter.drawEllipse(node.boundingRect().center(), node.boundingRect(
        ).width() / 2, node.boundingRect().width() / 2)

    @staticmethod
    def asGraphSides(node, painter, option, widget):
        color = Colors.White
        if node.isSelected():
            color = color.lighter(150)

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)
        # pen = QtGui.QPen(node.canvasRef().parent.styleSheetEditor.style.MainColor, 0.5)
        pen = QtGui.QPen(QtCore.Qt.black, 0.75)
        painter.setPen(pen)
        r = QtCore.QRectF(node.boundingRect())
        r.setWidth(r.width() - pen.width())
        r.setHeight(r.height() - pen.width())
        r.setX(pen.width())
        r.setY(r.y() + pen.width())
        painter.drawRoundedRect(r, node.sizes[4], node.sizes[5])
        pen = QtGui.QPen(Colors.AbsoluteBlack, 0.5)
        painter.setPen(pen)
        font = painter.font()
        nameRect = QtCore.QRectF(node.boundingRect())
        nameRect.setTop(node.boundingRect().top() + font.pointSize())
        painter.drawText(nameRect, QtCore.Qt.AlignTop |
                         QtCore.Qt.AlignHCenter, node.displayName)
        if option.state & QStyle.State_Selected:
            # pen.setColor(Colors.Yellow)
            pen.setColor(
                node.canvasRef().window().styleSheetEditor.style.MainColor)
            pen.setStyle(node.opt_pen_selected_type)
            pen.setWidth(pen.width() * 1.5)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(0, 0, 0, 0))
            r = QtCore.QRectF(node.boundingRect())
            r.setWidth(r.width() - pen.width())
            r.setHeight(r.height() - pen.width())
            r.setX(pen.width())
            r.setY(r.y() + pen.width())
            painter.drawRoundedRect(r, node.sizes[4], node.sizes[5])

"""@file PinPainter.py
"""
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Utils.Settings import *


# Determines how to paint a pin
class PinPainter(object):

    _execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
    _groupPen = QtGui.QPen(Colors.AbsoluteBlack, 0.5, QtCore.Qt.SolidLine)

    @staticmethod
    def asValuePin(pin, painter, option, widget):
        background_rect = QtCore.QRectF(1, 1, pin.width, pin.width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(
            QtCore.QPointF(w + 1, h + 1), pin.width / 2.5)
        if not pin._rawPin.hasConnections():
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
        painter.drawEllipse(background_rect)

    @staticmethod
    def asExecPin(pin, painter, option, widget):
        painter.setPen(PinPainter._execPen)
        if pin._rawPin.hasConnections():
            painter.setBrush(QtGui.QBrush(pin.color()))
        else:
            painter.setBrush(QtCore.Qt.NoBrush)
        arrow = QtGui.QPolygonF([QtCore.QPointF(2, 0.0),
                                 QtCore.QPointF(2 + pin.width / 2.0, 0.0),
                                 QtCore.QPointF(
                                     2 + pin.width, pin.height / 2.0),
                                 QtCore.QPointF(
                                     2 + pin.width / 2.0, pin.height),
                                 QtCore.QPointF(2, pin.height)])
        painter.drawPolygon(arrow)

    @staticmethod
    def asGroupPin(pin, painter, option, widget):
        painter.setPen(PinPainter._groupPen)
        painter.setBrush(QtGui.QBrush(Colors.AbsoluteBlack))
        # painter.setBrush(QtCore.Qt.NoBrush)
        if not pin.expanded:
            arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                     QtCore.QPointF(
                                         pin.width, pin.height / 2.0),
                                     QtCore.QPointF(0, pin.height)])
        else:
            arrow = QtGui.QPolygonF([QtCore.QPointF(pin.width / 2, pin.height),
                                     QtCore.QPointF(0, 0),
                                     QtCore.QPointF(pin.width, 0)])
        painter.drawPolygon(arrow)
        # painter.drawRect(0,0,pin.width,pin.height)

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

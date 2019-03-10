"""@file NodePainter.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QStyle
from Settings import *


## Determines how to paint the node
class NodePainter(object):

    @staticmethod
    def default(node, painter, option, widget):

        # painter.setPen(QtCore.Qt.NoPen)
        # painter.setBrush(QtCore.Qt.darkGray)

        color = node.color
        color.setAlpha(230)
        if node.isSelected():
            color = color.lighter(150)
        if node.isTemp:
            color = color.lighter(50)
            color.setAlpha(50)
        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)

        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        if option.state & QStyle.State_Selected:
            # pen.setColor(node.graph().parent.styleSheetEditor.style.MainColor)
            pen.setColor(Colors.Yellow)
            pen.setStyle(node.opt_pen_selected_type)
        painter.setPen(pen)
        painter.drawRoundedRect(node.boundingRect(), node.sizes[4], node.sizes[5])

        br = QtGui.QBrush()
        painter.setBrush(br)
        if node.label().isVisible():
            headColor = node.headColor
            if node.isTemp:
                headColor = headColor.lighter(50)
                headColor.setAlpha(50)
            r = QtCore.QRectF(node.boundingRect())
            r.setWidth(node.boundingRect().width() - 0.25)
            r.setHeight(node.label().h)
            r.setX(0.25)
            #r.moveTop(rect.top())
            b = QtGui.QLinearGradient(0, 0, r.width(), r.height())
            b.setColorAt(0, headColor.lighter(60))
            b.setColorAt(0.5, headColor)
            b.setColorAt(1, headColor.darker(50))
            painter.setPen(QtCore.Qt.NoPen)
            path = QtGui.QPainterPath()
            path.addRoundedRect(r, node.sizes[4], node.sizes[5])
            painter.fillPath(path, b)

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
            pen.setColor(Colors.Yellow)
            pen.setStyle(node.opt_pen_selected_type)
        painter.setPen(pen)
        painter.drawRoundedRect(node.boundingRect(), 7, 7)
        painter.setFont(node.label().opt_font)
        # pen.setColor(QtGui.QColor(*node.var.widget.color))
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 0.5))
        textRect = node.boundingRect()
        textRect.setWidth(textRect.width() - 10)
        painter.drawText(textRect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, node.displayName)

    @staticmethod
    def asReruteNode(node, painter, option, widget):
        color = node.color
        color.setAlpha(255)
        #if node.isSelected():
        color = color.lighter(100)
        if node.isTemp:
            color = color.lighter(50)
            color.setAlpha(50)
        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)

        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        width = pen.width()
        if option.state & QStyle.State_Selected:
            # pen.setColor(node.graph().parent.styleSheetEditor.style.MainColor)
            pen.setColor(Colors.Yellow)
            pen.setStyle(node.opt_pen_selected_type)
            pen.setWidth(width * 2)
        painter.setPen(pen)
        painter.drawEllipse(node.boundingRect().center(), node.boundingRect().width() / 2, node.boundingRect().width() / 2)

    @staticmethod
    def asGraphSides(node, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        # if node.isSelected():
        #    color = color.lighter(150)

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(40, 40), 300)
        linearGrad.setColorAt(0, color)
        linearGrad.setColorAt(1, color.lighter(180))
        br = QtGui.QBrush(linearGrad)
        painter.setBrush(br)
        # pen = QtGui.QPen(node.graph().parent.styleSheetEditor.style.MainColor, 0.5)
        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        painter.setPen(pen)
        painter.drawRoundedRect(node.boundingRect(), node.sizes[4], node.sizes[5])
        pen = QtGui.QPen(Colors.Yellow, 0.5)
        painter.setPen(pen)
        font = painter.font()
        nameRect = QtCore.QRectF(node.boundingRect())
        nameRect.setTop(node.boundingRect().top() + font.pointSize())
        painter.drawText(nameRect, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter, node.displayName)

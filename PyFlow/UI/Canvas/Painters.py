# Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import atan2, degrees
from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import QStyle

from PyFlow import getPinFromData

from PyFlow.UI.Canvas.UICommon import *
from PyFlow.Core.Common import *

from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.UI.Utils.stylesheet import Colors

InvalidNodePenColor = Colors.Red
ExposedPropertiesColor = Colors.NodeNameRectBlue


# Determines how to paint the node
class NodePainter(object):

    @staticmethod
    def drawDeprecated(node, painter, option, widget):
        if node.isDeprecated():
            font = painter.font()
            font.setPointSize(6)
            painter.setFont(font)
            textRect = node.boundingRect()
            textRect.setTop(textRect.height() - 10)
            painter.fillRect(textRect, Colors.Red.darker(130))
            painter.drawText(textRect, QtCore.Qt.AlignCenter |
                             QtCore.Qt.AlignVCenter, "Deprecated")

    @staticmethod
    def drawExperimental(node, painter, option, widget):
        if node.isExperimental():
            font = painter.font()
            font.setPointSize(6)
            painter.setFont(font)
            textRect = node.boundingRect()
            textRect.setTop(textRect.height() - 10)
            painter.fillRect(textRect, Colors.Yellow.darker(180))
            painter.drawText(textRect, QtCore.Qt.AlignCenter |
                             QtCore.Qt.AlignVCenter, "Experimental")

    @staticmethod
    def drawResizeHandles(node, painter, option, widget):
        if node.resizable and not node.collapsed:
            pen = QtGui.QPen()
            height = node.geometry().height()
            width = node.geometry().width()
            rf = node.roundness * 2
            pen.setColor(editableStyleSheet().MainColor)
            pen.setStyle(node.optPenSelectedType)
            painter.setPen(pen)

            # left strip
            if node.resizeStrips[0]:
                painter.drawLine(0, rf / 2, 0, height - rf / 2)
            # top strip
            if node.resizeStrips[1]:
                painter.drawLine(rf / 2, 0, width - rf / 2, 0)
            # right strip
            if node.resizeStrips[2]:
                painter.drawLine(width, rf / 2, width, height - rf / 2)
            # bottom strip
            if node.resizeStrips[3]:
                painter.drawLine(rf / 2, height, width - rf / 2, height)

            # bottom right strip
            if node.resizeStrips[4]:
                painter.drawArc(width - rf, height - rf, rf, rf, 0, -90 * 16)

            # bottom left strip
            if node.resizeStrips[5]:
                painter.drawArc(0, height - rf, rf, rf, -90 * 16, -90 * 16)

            # top left strip
            if node.resizeStrips[6]:
                painter.drawArc(0, 0, rf, rf, 90 * 16, 90 * 16)

            # top right strip
            if node.resizeStrips[7]:
                painter.drawArc(width - rf, 0, rf, rf, 90 * 16, -90 * 16)

    @staticmethod
    def asCommentNode(node, painter, option, widget):
        frame = QtCore.QRectF(QtCore.QPointF(0, 0), node.geometry().size())
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

        color = Colors.NodeBackgrounds
        if node.isSelected():
            color = color.lighter(150)

        painter.setBrush(node.color)
        pen = QtGui.QPen(QtCore.Qt.black, 0.75)
        if option.state & QStyle.State_Selected:
            pen.setColor(editableStyleSheet().MainColor)
            pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawRoundedRect(frame, node.roundness, node.roundness)

        if option.state & QStyle.State_Selected:
            pen.setColor(editableStyleSheet().MainColor)
            pen.setStyle(node.optPenSelectedType)
            pen.setWidth(pen.width() * 1.5)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        painter.drawRoundedRect(frame, node.roundness, node.roundness)
        painter.drawLine(frame.left() + 5, node.labelHeight,
                         frame.right() - 5, node.labelHeight)
        NodePainter.drawResizeHandles(node, painter, option, widget)

    @staticmethod
    def drawGroups(node, painter, option, widget):
        inputsOffset = QtCore.QPointF(-2, 0)
        outputsOffset = QtCore.QPointF(2, 0)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 200), 0.5))
        for grp in node.groups["input"].values():
            if grp.hovered and grp.expanded:
                if grp.numPins() > 0:
                    grpPos = grp.geometry().bottomLeft()
                    lastPinPos = grp._pins[grp.numPins(
                    ) - 1].geometry().bottomLeft()
                    painter.drawLine(grpPos, grpPos + inputsOffset)
                    painter.drawLine(grpPos + inputsOffset,
                                     lastPinPos + inputsOffset)
                    painter.drawLine(lastPinPos + inputsOffset, lastPinPos)

        for grp in node.groups["output"].values():
            if grp.hovered and grp.expanded:
                if grp.numPins() > 0:
                    grpPos = grp.geometry().bottomRight()
                    lastPinPos = grp._pins[grp.numPins(
                    ) - 1].geometry().bottomRight()
                    painter.drawLine(grpPos, grpPos + outputsOffset)
                    painter.drawLine(grpPos + outputsOffset,
                                     lastPinPos + outputsOffset)
                    painter.drawLine(lastPinPos + outputsOffset, lastPinPos)

    @staticmethod
    def default(node, painter, option, widget):
        frame = QtCore.QRectF(QtCore.QPointF(0, 0), node.geometry().size())
        # use 3 levels of detail
        lod = node.canvasRef().getCanvasLodValueFromCurrentScale()
        SWITCH_LOD = editableStyleSheet().NodeSwitch[0]

        color = node.color

        color.setAlpha(230)
        if node.isSelected():
            color = color.lighter(150)
        if node.isTemp:
            color = color.lighter(50)
            color.setAlpha(50)

        br = QtGui.QBrush(color)
        painter.setBrush(br)

        pen = QtGui.QPen(QtCore.Qt.black, 0.5)
        painter.setPen(QtCore.Qt.NoPen)

        r = frame
        if lod < SWITCH_LOD:
            r.setWidth(r.width() - pen.width() / 2)
            r.setHeight(r.height() - pen.width() / 2)
            r.setX(pen.width() / 2)
            r.setY(r.y() + pen.width() / 2)
            painter.drawRoundedRect(r, node.roundness, node.roundness)
        else:
            painter.drawRect(r)

        br = QtGui.QBrush()
        painter.setBrush(br)
        if node.drawlabel:
            lr = QtCore.QRectF(r)
            lr.setHeight(node.labelHeight + NodeDefaults().CONTENT_MARGINS / 2)
            headColor = node.headColor
            if node.isTemp:
                headColor = headColor.lighter(50)
                headColor.setAlpha(50)
            if lod < SWITCH_LOD:
                b = QtGui.QLinearGradient(0, 0, lr.width(), 0)
                b.setColorAt(0, headColor.lighter(60))
                b.setColorAt(0.5, headColor)
                b.setColorAt(1, headColor.darker(50))
                path = QtGui.QPainterPath()
                path.setFillRule(QtCore.Qt.WindingFill)
                path.addRoundedRect(lr, node.roundness, node.roundness)
                lr.setY(lr.y() + node.roundness)
                path.addRect(lr)
                painter.fillPath(path, b)
            else:
                painter.fillRect(lr, headColor)

        if not node.isCallable() and node._rawNode.bCacheEnabled or node._rawNode.__class__.__name__=="graphOutputs":
            NodePainter.drawState(node, painter, pen, lod, SWITCH_LOD, r)

        if not node.isValid():
            pen.setColor(InvalidNodePenColor)
            pen.setStyle(node.optPenErrorType)
            pen.setWidth(pen.width() * 1.5)
        elif not node.bExposeInputsToCompound:
            if option.state & QStyle.State_Selected:
                pen.setColor(editableStyleSheet().MainColor)
                pen.setStyle(node.optPenSelectedType)
                pen.setWidth(pen.width() * 1.5)
        else:
            pen.setColor(ExposedPropertiesColor)
            pen.setStyle(node.optPenSelectedType)
            pen.setWidth(pen.width() * 1.5)

        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        if lod < SWITCH_LOD:
            painter.drawRoundedRect(r, node.roundness, node.roundness)
        else:
            painter.drawRect(r)

        NodePainter.drawResizeHandles(node, painter, option, widget)
        NodePainter.drawGroups(node, painter, option, widget)
        NodePainter.drawDeprecated(node, painter, option, widget)
        NodePainter.drawExperimental(node, painter, option, widget)

    @staticmethod
    def drawState(node, painter, pen, lod, SWITCH_LOD, r):
        prevWidth = pen.width()  
        paint = False
        if node.computing:
            pen.setColor(Colors.Yellow)
            pen.setStyle(node.optPenSelectedType)
            pen.setWidth(prevWidth * 2)
            paint = True
        else:        
            if node._rawNode.isDirty():
                pen.setColor(Colors.Orange)
                pen.setStyle(node.optPenSelectedType)
                pen.setWidth(prevWidth * 2)
                paint = True
            else:
                pen.setColor(Colors.Green)
                pen.setStyle(node.optPenSelectedType)
                pen.setWidth(prevWidth * 2)
                paint = True         

        if paint and node.isValid():
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(0, 0, 0, 0))
            rect = QtCore.QRectF(r)
            if lod < SWITCH_LOD:
                rect.setWidth(rect.width() - pen.width() / 2)
                rect.setHeight(rect.height() - pen.width() / 2)
                rect.setX(pen.width() / 2)
                rect.setY(rect.y() + pen.width() / 2)            
                painter.drawRoundedRect(rect, node.roundness, node.roundness)
            else:
                painter.drawRect(r)    
        pen.setWidth(prevWidth)

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
            pen.setColor(editableStyleSheet().MainColor)
            pen.setStyle(node.optPenSelectedType)
        painter.setPen(pen)
        painter.drawRoundedRect(node.boundingRect(),
                                node.roundness, node.roundness)
        painter.setFont(node.nodeNameFont)
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 0.5))
        textRect = node.boundingRect()
        textRect.setWidth(textRect.width() - 10)
        painter.drawText(textRect, QtCore.Qt.AlignCenter |
                         QtCore.Qt.AlignVCenter, node.var.name)

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
            pen.setColor(editableStyleSheet().MainColor)
            pen.setStyle(node.optPenSelectedType)
            pen.setWidth(width * 1.5)
        painter.setPen(pen)
        painter.drawEllipse(node.boundingRect().center(
        ), node.drawRect.width() / 2, node.drawRect.width() / 2)


# Determines how to paint a pin
class PinPainter(object):

    _execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
    _valuePinNamePen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
    _groupPen = QtGui.QPen(Colors.AbsoluteBlack, 0.5, QtCore.Qt.SolidLine)

    @staticmethod
    def asValuePin(pin, painter, option, widget):
        lod = pin.owningNode().canvasRef().getCanvasLodValueFromCurrentScale()
        SWITCH_LOD = editableStyleSheet().PinSwitch[0]

        frame = QtCore.QRectF(QtCore.QPointF(0, 0), pin.geometry().size())

        w = frame.width() / 2
        h = frame.height() / 2
        halfPinSize = pin.pinSize / 2

        if lod < SWITCH_LOD and not pin.bLabelHidden:
            painter.setFont(pin._font)
            textWidth = QtGui.QFontMetrics(
                painter.font()).horizontalAdvance(pin.displayName())
            textHeight = QtGui.QFontMetrics(painter.font()).height()
            x = 1 + pin.pinSize + halfPinSize
            if pin.direction == PinDirection.Output:
                x = frame.width() - textWidth - pin.pinSize - 1
            yCenter = textHeight - textHeight / 3
            painter.setPen(QtGui.QPen(
                pin.labelColor, 0.5, QtCore.Qt.SolidLine))
            painter.drawText(x, yCenter, pin.displayName())

        pinCenter = pin.pinCenter()
        radialGrad = QtGui.QRadialGradient(
            pinCenter.x(), pinCenter.y() - 0.3, halfPinSize * 0.8)
        if not pin._rawPin.hasConnections():
            radialGrad.setColorAt(0, pin.color().darker(280))
            radialGrad.setColorAt(0.5, pin.color().darker(280))
            radialGrad.setColorAt(0.65, pin.color().lighter(130))
            radialGrad.setColorAt(1, pin.color().lighter(70))
        else:
            radialGrad.setColorAt(0, pin.color())
            radialGrad.setColorAt(1, pin.color())

        painter.setPen(QtCore.Qt.NoPen)
        if pin.hovered:
            radialGrad.setColorAt(1, pin.color().lighter(200))
            painter.setBrush(QtGui.QColor(128, 128, 128, 30))
            painter.drawRoundedRect(frame, 3, 3)
        painter.setBrush(radialGrad)
        painter.drawEllipse(pinCenter.x() - halfPinSize,
                            pinCenter.y() - halfPinSize, pin.pinSize, pin.pinSize)

    @staticmethod
    def asExecPin(pin, painter, option, widget):
        lod = pin.owningNode().canvasRef().getCanvasLodValueFromCurrentScale()
        SWITCH_LOD = editableStyleSheet().PinSwitch[0]
        frame = QtCore.QRectF(QtCore.QPointF(0, 0), pin.geometry().size())
        w = frame.width() / 2
        h = frame.height() / 2
        halfPinSize = pin.pinSize / 2
        painter.setFont(pin._font)
        painter.setPen(PinPainter._execPen)

        if lod < SWITCH_LOD and not pin.bLabelHidden:
            textWidth = QtGui.QFontMetrics(
                painter.font()).horizontalAdvance(pin.displayName())
            textHeight = QtGui.QFontMetrics(painter.font()).height()
            x = 1 + pin.pinSize + halfPinSize
            if pin.direction == PinDirection.Output:
                x = frame.width() - textWidth - pin.pinSize - 1
            yCenter = textHeight - textHeight / 3
            painter.setPen(QtGui.QPen(
                pin.labelColor, 0.5, QtCore.Qt.SolidLine))
            painter.drawText(x, yCenter, pin.displayName())

        if pin._rawPin.hasConnections():
            painter.setBrush(QtGui.QBrush(pin.color()))
        else:
            painter.setBrush(QtCore.Qt.NoBrush)
        pinCenter = pin.pinCenter()
        xOffset = pinCenter.x() - \
            pin.pinSize if pin.direction == PinDirection.Input else pinCenter.x() - \
            pin.pinSize * 0.8
        arrow = QtGui.QPolygonF([QtCore.QPointF(2, 0.0),
                                 QtCore.QPointF(2 + pin.pinSize / 2.0, 0.0),
                                 QtCore.QPointF(2 + pin.pinSize,
                                                pin.pinSize / 2.0),
                                 QtCore.QPointF(
                                     2 + pin.pinSize / 2.0, pin.pinSize),
                                 QtCore.QPointF(2, pin.pinSize)]).translated(xOffset, 1)
        painter.drawPolygon(arrow)
        if pin.hovered:
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor(128, 128, 128, 30))
            painter.drawRoundedRect(frame, 3, 3)

    @staticmethod
    def asGroupPin(pin, painter, option, widget):
        painter.setPen(PinPainter._groupPen)
        painter.setBrush(QtGui.QBrush(Colors.AbsoluteBlack))
        # painter.setBrush(QtCore.Qt.NoBrush)
        if not pin.expanded:
            arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                     QtCore.QPointF(
                                         pin.pinSize, pin.pinSize / 2.0),
                                     QtCore.QPointF(0, pin.pinSize)])
        else:
            arrow = QtGui.QPolygonF([QtCore.QPointF(pin.pinSize / 2, pin.pinSize),
                                     QtCore.QPointF(0, 0),
                                     QtCore.QPointF(pin.pinSize, 0)])
        painter.drawPolygon(arrow)

    @staticmethod
    def asArrayPin(pin, painter, option, widget):
        lod = pin.owningNode().canvasRef().getCanvasLodValueFromCurrentScale()
        SWITCH_LOD = editableStyleSheet().PinSwitch[0]
        gridSize = 3
        cellW = pin.pinSize / gridSize
        cellH = pin.pinSize / gridSize
        pinCenter = pin.pinCenter()
        halfPinSize = pin.pinSize / 2

        painter.setBrush(QtGui.QBrush(pin.color()))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.2))
        for row in range(gridSize):
            for column in range(gridSize):
                x = row * cellW + pinCenter.x() - halfPinSize
                y = column * cellH + pinCenter.y() - halfPinSize
                painter.drawRect(x, y, cellW, cellH)

        if lod < SWITCH_LOD and not pin.bLabelHidden:
            frame = QtCore.QRectF(QtCore.QPointF(0, 0), pin.geometry().size())
            halfPinSize = pin.pinSize / 2
            painter.setFont(pin._font)
            textWidth = QtGui.QFontMetrics(
                painter.font()).horizontalAdvance(pin.displayName())
            textHeight = QtGui.QFontMetrics(painter.font()).height()
            x = 1 + pin.pinSize + halfPinSize
            if pin.direction == PinDirection.Output:
                x = frame.width() - textWidth - pin.pinSize - 1
            yCenter = textHeight - textHeight / 3
            painter.setPen(PinPainter._valuePinNamePen)
            painter.drawText(x, yCenter, pin.name)

            if pin.hovered:
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(QtGui.QColor(128, 128, 128, 30))
                painter.drawRoundedRect(frame, 3, 3)

    @staticmethod
    def asDictPin(pin, painter, option, widget):
        lod = pin.owningNode().canvasRef().getCanvasLodValueFromCurrentScale()
        SWITCH_LOD = editableStyleSheet().PinSwitch[0]
        cellW = pin.pinSize / 3
        cellH = pin.pinSize / 3
        pinCenter = pin.pinCenter()
        halfPinSize = pin.pinSize / 2

        painter.setBrush(QtGui.QBrush(pin.color()))
        keyPin = findPinClassByType(pin._rawPin._keyType)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.2))
        for row in range(3):
            x = pinCenter.x() - halfPinSize
            y = row * cellH + (halfPinSize / 2) + pin.pinCircleDrawOffset.y()
            painter.setBrush(QtGui.QBrush(pin.color()))
            painter.drawRect(x + cellW, y, cellW * 2, cellH)
            if keyPin:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(*keyPin.color())))
            painter.drawRect(x, y, cellW, cellH)

        if lod < SWITCH_LOD and not pin.bLabelHidden:
            frame = QtCore.QRectF(QtCore.QPointF(0, 0), pin.geometry().size())
            halfPinSize = pin.pinSize / 2
            painter.setFont(pin._font)
            textWidth = QtGui.QFontMetrics(
                painter.font()).horizontalAdvance(pin.displayName())
            textHeight = QtGui.QFontMetrics(painter.font()).height()
            x = 1 + pin.pinSize + halfPinSize
            if pin.direction == PinDirection.Output:
                x = frame.width() - textWidth - pin.pinSize - 1
            yCenter = textHeight - textHeight / 3
            painter.setPen(PinPainter._valuePinNamePen)
            painter.drawText(x, yCenter, pin.name)

            if pin.hovered:
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(QtGui.QColor(128, 128, 128, 30))
                painter.drawRoundedRect(frame, 3, 3)

# Determines how to paint a connection:
class ConnectionPainter(object):

    @staticmethod
    def linearPath(path, closed=False):
        mPath = QtGui.QPainterPath()
        mPath.moveTo(path[0])
        for point in path[1:]:
            mPath.lineTo(point)
        return mPath

    @staticmethod
    def chanferPath(path, offset, closed=False):
        mPath = []
        for i, point in enumerate(path):
            prevPoint = nextPoint = QtGui.QVector2D(point)
            currPoint = QtGui.QVector2D(point)
            if i != len(path) - 1:
                nextPoint = QtGui.QVector2D(path[i + 1])
            elif closed:
                nextPoint = QtGui.QVector2D(path[0])
            if i != 0:
                prevPoint = QtGui.QVector2D(path[i - 1])
            elif closed:
                prevPoint = QtGui.QVector2D(path[-1])

            fDist = nextPoint - currPoint
            bDist = currPoint - prevPoint

            maxLen = max(0, min(fDist.length() / 2, (bDist.length()) / 2))

            dot = fDist.x() * bDist.x() + fDist.y() * bDist.y()      # dot product
            det = fDist.x() * bDist.y() - fDist.y() * bDist.x()      # determinant
            angle = degrees(atan2(det, dot))  # atan2(y, x) or atan2(sin, cos)

            if abs(angle) > 45:
                n = currPoint + fDist.normalized() * maxLen
                p = currPoint - bDist.normalized() * maxLen
                if i == 0 and not closed:
                    mPath.append(point)
                elif i == 0 and closed:
                    mPath.append(QtCore.QPointF(p.x(), p.y()))
                    mPath.append(QtCore.QPointF(n.x(), n.y()))
                elif i != len(path) - 1 or closed:
                    mPath.append(QtCore.QPointF(p.x(), p.y()))
                    mPath.append(QtCore.QPointF(n.x(), n.y()))
                elif i == len(path) - 1 and not closed:
                    mPath.append(point)
                if i == len(path) - 1 and closed:
                    n = nextPoint - fDist.normalized() * maxLen
                    mPath.append(QtCore.QPointF(n.x(), n.y()))
            else:
                mPath.append(point)

        return mPath

    @staticmethod
    def roundCornersPath(path, roundness, closed=False, highlightedSegment=-1):
        mPath = QtGui.QPainterPath()
        highlightedSegmentPath = QtGui.QPainterPath()
        for i, point in enumerate(path):
            prevPoint = nextPoint = QtGui.QVector2D(point)
            currPoint = QtGui.QVector2D(point)
            if i != len(path) - 1:
                nextPoint = QtGui.QVector2D(path[i + 1])
            elif closed:
                nextPoint = QtGui.QVector2D(path[0])
            if i != 0:
                prevPoint = QtGui.QVector2D(path[i - 1])
            elif closed:
                prevPoint = QtGui.QVector2D(path[-1])

            fDist = nextPoint - currPoint
            bDist = currPoint - prevPoint

            xRoundnes = min(min(roundness, fDist.length() / 2.0), bDist.length() / 2.0)

            n = currPoint + fDist.normalized() * xRoundnes
            p = currPoint - bDist.normalized() * xRoundnes
            if i == 0 and not closed:
                mPath.moveTo(point)
            elif i == 0 and closed:
                mPath.moveTo(QtCore.QPointF(p.x(), p.y()))
                mPath.quadTo(point, QtCore.QPointF(n.x(), n.y()))

            elif i != len(path) - 1 or closed:
                mPath.lineTo(QtCore.QPointF(p.x(), p.y()))
                mPath.quadTo(point, QtCore.QPointF(n.x(), n.y()))

            elif i == len(path) - 1 and not closed:
                mPath.lineTo(point)
            if i == len(path) - 1 and closed:
                n = nextPoint - fDist.normalized() * xRoundnes
                mPath.lineTo(QtCore.QPointF(n.x(), n.y()))

            if i == highlightedSegment:
                if i != 0:
                    highlightedSegmentPath.moveTo(QtCore.QPointF(p.x(), p.y()))
                    highlightedSegmentPath.quadTo(point, QtCore.QPointF(n.x(), n.y()))
                else:
                    highlightedSegmentPath.moveTo(point)
                currPoint = QtGui.QVector2D(path[i + 1])
                nextPoint = QtGui.QVector2D(path[i + 2])
                prevPoint = QtGui.QVector2D(point.x(), point.y())
                fDist = nextPoint - currPoint
                bDist = currPoint - prevPoint
                xRoundnes = min(min(roundness, fDist.length() / 2.0), bDist.length() / 2.0)

                n = currPoint + fDist.normalized() * xRoundnes
                p = currPoint - bDist.normalized() * xRoundnes
                highlightedSegmentPath.lineTo(QtCore.QPointF(p.x(), p.y()))
                highlightedSegmentPath.quadTo(QtCore.QPointF(currPoint.x(), currPoint.y()), QtCore.QPointF(n.x(), n.y()))

        return mPath, highlightedSegmentPath

    @staticmethod
    def BasicCircuit(p1, p2,
                     offset=20,
                     roundness=5,
                     sameSide=0,
                     lod=0,
                     complexLine=False,
                     vOffset=0,
                     hOffsetL=0,
                     vOffsetSShape=0,
                     hOffsetR=0,
                     hOffsetRSShape=0,
                     hOffsetLSShape=0,
                     snapVToFirst=False,
                     snapVToSecond=False,
                     highlightedSegment=-1):
        SWITCH_LOD = editableStyleSheet().ConnectionSwitch[0]
        offset1 = offset
        offset2 = -offset
        if sameSide == 1:
            offset2 = offset
        elif sameSide == -1:
            offset1 = -offset

        xDistance = (p2.x() + offset2) - (p1.x() + offset1)
        midPointY = p2.y() + ((p1.y() - p2.y()) / 2.0) + vOffsetSShape

        path = []
        path.append(p1)
        if xDistance > 0 or sameSide == -1:
            if snapVToSecond:
                vOffset = p2.y() - p1.y()
            elif snapVToFirst:
                vOffset = 0

            if not snapVToFirst:
                offset1 += hOffsetL
            if not snapVToSecond:
                offset2 += hOffsetR

            if abs(vOffset) > 0:
                path.append(QtCore.QPointF(p1.x() + offset1, p1.y()))
                path.append(QtCore.QPointF(p1.x() + offset1, p1.y() + vOffset))

            path.append(QtCore.QPointF(p2.x() + offset2, p1.y() + vOffset))
            path.append(QtCore.QPointF(p2.x() + offset2, p2.y()))
            path.append(p2)
        else:
            offset1 += hOffsetRSShape
            offset2 += hOffsetLSShape
            path.append(QtCore.QPointF(p1.x() + offset1, p1.y()))
            path.append(QtCore.QPointF(p1.x() + offset1, midPointY))
            path.append(QtCore.QPointF(p2.x() + offset2, midPointY))
            path.append(QtCore.QPointF(p2.x() + offset2, p2.y()))
            path.append(p2)

        if complexLine:
            path = ConnectionPainter.chanferPath(path, offset)

        section = None
        if lod >= SWITCH_LOD:
            mPath = ConnectionPainter.linearPath(path)
        else:
            mPath, section = ConnectionPainter.roundCornersPath(path, roundness, highlightedSegment=highlightedSegment)
        return mPath, path, section

    @staticmethod
    def Cubic(p1, p2, defOffset=150, lod=0):
        SWITCH_LOD = editableStyleSheet().ConnectionSwitch[0]
        mPath = QtGui.QPainterPath()

        xDistance = p2.x() - p1.x()
        vDistance = p2.y() - p1.y()
        offset = abs(xDistance) * 0.5
        if abs(xDistance) < defOffset:
            offset = defOffset / 2
        if abs(vDistance) < 20:
            offset = abs(xDistance) * 0.3
        mPath.moveTo(p1)
        if lod >= SWITCH_LOD:
            offset = 20
        if xDistance < 0:
            cp1 = QtCore.QPointF(p1.x() + offset, p1.y())
            cp2 = QtCore.QPointF(p2.x() - offset, p2.y())
        else:
            cp2 = QtCore.QPointF(p2.x() - offset, p2.y())
            cp1 = QtCore.QPointF(p1.x() + offset, p1.y())
        if lod >= SWITCH_LOD:
            mPath = ConnectionPainter.linearPath([p1, cp1, cp2, p2])
        else:
            mPath.cubicTo(cp1, cp2, p2)

        return mPath

    @staticmethod
    def Linear(p1, p2, defOffset=150, roundness=5, lod=0):
        SWITCH_LOD = editableStyleSheet().ConnectionSwitch[0]

        cp1 = QtCore.QPointF(p1.x() + defOffset, p1.y())
        cp2 = QtCore.QPointF(p2.x() - defOffset, p2.y())

        if lod >= SWITCH_LOD:
            mPath = ConnectionPainter.linearPath([p1, cp1, cp2, p2])
        else:
            mPath = ConnectionPainter.roundCornersPath([p1, cp1, cp2, p2], roundness)

        return mPath

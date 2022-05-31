## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import weakref
from uuid import UUID, uuid4

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsPathItem
from Qt.QtWidgets import QGraphicsEllipseItem
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QStyle

from PyFlow.UI.Utils.stylesheet import editableStyleSheet, Colors, ConnectionTypes
from PyFlow.UI.Canvas.UICommon import NodeDefaults
from PyFlow.UI.Canvas.Painters import ConnectionPainter
from PyFlow.Core.Common import *



# UIConnection between pins
class UIConnection(QGraphicsPathItem):
    """UIConnection is a cubic spline curve. It represents connection between two pins.
    """
    def __init__(self, source, destination, canvas):
        QGraphicsPathItem.__init__(self)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        self._menu = QMenu()
        self.actionDisconnect = self._menu.addAction("Disconnect")
        self.actionDisconnect.triggered.connect(self.kill)
        self._uid = uuid4()
        self.canvasRef = weakref.ref(canvas)
        self.source = weakref.ref(source)
        self.destination = weakref.ref(destination)
        self.drawSource = self.source()
        self.drawDestination = self.destination()

        # Overrides for getting endpoints positions
        # if None - pin centers will be used
        self.sourcePositionOverride = None
        self.destinationPositionOverride = None

        self.mPath = QtGui.QPainterPath()

        self.cp1 = QtCore.QPointF(0.0, 0.0)
        self.cp2 = QtCore.QPointF(0.0, 0.0)

        self.setZValue(NodeDefaults().Z_LAYER - 1)

        self.color = self.source().color()
        self.selectedColor = self.color.lighter(150)

        self.thickness = 1
        self.thicknessMultiplier = 1
        if source.isExec():
            self.thickness = 2

        self.pen = QtGui.QPen(self.color, self.thickness, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        self.setPen(self.pen)

        self.source().update()
        self.destination().update()
        self.fade = 0.0
        self.source().uiConnectionList.append(self)
        self.destination().uiConnectionList.append(self)
        self.source().pinConnected(self.destination())
        self.destination().pinConnected(self.source())
        self.prevPos = None
        self.linPath = None
        self.hOffsetL = 0.0
        self.hOffsetR = 0.0
        self.hOffsetLSShape = 0.0
        self.hOffsetRSShape = 0.0
        self.vOffset = 0.0
        self.vOffsetSShape = 0.0
        self.offsetting = 0
        self.snapVToFirst = True
        self.snapVToSecond = False
        self.sShape = False
        self.sameSide = 0
        self.hoverSegment = -1
        self.pressedSegment = -1
        if self.source().isExec():
            self.bubble = QGraphicsEllipseItem(-2.5, -2.5, 5, 5, self)
            self.bubble.setBrush(self.color)
            self.bubble.setPen(self.pen)

            point = self.mPath.pointAtPercent(0.0)
            self.bubble.setPos(point)

            self.bubble.hide()
            self.source()._rawPin.onExecute.connect(self.performEvaluationFeedback)
            self.shouldAnimate = False
            self.timeline = QtCore.QTimeLine(2000)
            self.timeline.setFrameRange(0, 100)
            self.timeline.frameChanged.connect(self.timelineFrameChanged)
            self.timeline.setLoopCount(0)

    def performEvaluationFeedback(self, *args, **kwargs):
        if self.timeline.state() == QtCore.QTimeLine.State.NotRunning:
            self.shouldAnimate = True
            # spawn bubble
            self.bubble.show()
            self.timeline.start()

    def timelineFrameChanged(self, frameNum):
        percentage = currentProcessorTime() - self.source()._rawPin.getLastExecutionTime()
        self.shouldAnimate = percentage < 0.5
        point = self.mPath.pointAtPercent(float(frameNum) / float(self.timeline.endFrame()))
        self.bubble.setPos(point)
        if not self.shouldAnimate:
            self.timeline.stop()
            self.bubble.hide()

    def setSelected(self, value):
        super(UIConnection, self).setSelected(value)

    def isUnderCollapsedComment(self):
        srcNode = self.source().owningNode()
        dstNode = self.destination().owningNode()
        srcComment = srcNode.owningCommentNode
        dstComment = dstNode.owningCommentNode
        if srcComment is not None and dstComment is not None and srcComment == dstComment and srcComment.collapsed:
            return True
        return False

    def isUnderActiveGraph(self):
        return self.canvasRef().graphManager.activeGraph() == self.source()._rawPin.owningNode().graph()

    def __repr__(self):
        return "{0} -> {1}".format(self.source().getFullName(), self.destination().getFullName())

    def setColor(self, color):
        self.pen.setColor(color)
        self.color = color

    def updateEndpointsPositions(self):
        srcNode = self.source().owningNode()
        dstNode = self.destination().owningNode()

        srcComment = srcNode.owningCommentNode
        if srcComment is not None:
            # if comment is collapsed or under another comment, move point to top most collapsed comment's right side
            srcNodeUnderCollapsedComment = srcComment.isUnderCollapsedComment()
            topMostCollapsedComment = srcNode.getTopMostOwningCollapsedComment()
            if srcComment.collapsed:
                rightSideEndpointGetter = srcComment.getRightSideEdgesPoint
                if srcNodeUnderCollapsedComment:
                    rightSideEndpointGetter = topMostCollapsedComment.getRightSideEdgesPoint
                self.sourcePositionOverride = rightSideEndpointGetter
            else:
                if srcNodeUnderCollapsedComment:
                    self.sourcePositionOverride = topMostCollapsedComment.getRightSideEdgesPoint
                else:
                    self.sourcePositionOverride = None
        else:
            # if no comment return source point back to pin
            self.sourcePositionOverride = None

        # Same for right hand side
        dstComment = dstNode.owningCommentNode
        if dstComment is not None:
            dstNodeUnderCollapsedComment = dstComment.isUnderCollapsedComment()
            topMostCollapsedComment = dstNode.getTopMostOwningCollapsedComment()
            if dstComment.collapsed:
                rightSideEndpointGetter = dstComment.getLeftSideEdgesPoint
                if dstNodeUnderCollapsedComment:
                    rightSideEndpointGetter = topMostCollapsedComment.getLeftSideEdgesPoint
                self.destinationPositionOverride = rightSideEndpointGetter
            else:
                if dstNodeUnderCollapsedComment:
                    self.destinationPositionOverride = topMostCollapsedComment.getLeftSideEdgesPoint
                else:
                    self.destinationPositionOverride = None
        else:
            self.destinationPositionOverride = None

    def Tick(self):
        # check if this instance represents existing connection
        # if not - destroy
        if not arePinsConnected(self.source()._rawPin, self.destination()._rawPin):
            self.canvasRef().removeConnection(self)

        if self.drawSource.isExec() or self.drawDestination.isExec():
            if self.thickness != 2:
                self.thickness = 2
                self.pen.setWidthF(self.thickness)

        if self.isSelected():
            self.pen.setColor(self.selectedColor)
        else:
            self.pen.setColor(self.color)
        self.update()

    def contextMenuEvent(self, event):
        self._menu.exec_(event.screenPos())

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self._uid in self.canvasRef().connections:
            self.canvasRef().connections[value] = self.canvasRef().connections.pop(self._uid)
            self._uid = value

    def applyJsonData(self, data):
        hOffsetL = data['hOffsetL']
        if hOffsetL is not None:
            self.hOffsetL = float(hOffsetL)
        hOffsetR = data['hOffsetR']
        if hOffsetR is not None:
            self.hOffsetR = float(hOffsetR)
        hOffsetLSShape = data['hOffsetLSShape']
        if hOffsetLSShape is not None:
            self.hOffsetLSShape = float(hOffsetLSShape)
        hOffsetRSShape = data['hOffsetRSShape']
        if hOffsetRSShape is not None:
            self.hOffsetRSShape = float(hOffsetRSShape)
        vOffset = data['vOffset']
        if vOffset is not None:
            self.vOffset = float(vOffset)
        vOffsetSShape = data['vOffsetSShape']
        if vOffsetSShape is not None:
            self.vOffsetSShape = float(vOffsetSShape)
        snapVToFirst = data['snapVToFirst']
        if snapVToFirst is not None:
            self.snapVToFirst = bool(snapVToFirst)
        snapVToSecond = data['snapVToSecond']
        if snapVToSecond is not None:
            self.snapVToSecond = bool(snapVToSecond)

        self.getEndPoints()

    def serialize(self):
        script = {'sourceUUID': str(self.source().uid),
                  'destinationUUID': str(self.destination().uid),
                  'sourceName': self.source()._rawPin.getFullName(),
                  'destinationName': self.destination()._rawPin.getFullName(),
                  'uuid': str(self.uid),
                  'hOffsetL': str(self.hOffsetL),
                  'hOffsetR': str(self.hOffsetR),
                  'hOffsetLSShape': str(self.hOffsetLSShape),
                  'hOffsetRSShape': str(self.hOffsetRSShape),
                  'vOffset': str(self.vOffset),
                  'vOffsetSShape': str(self.vOffsetSShape),
                  'snapVToFirst': int(self.snapVToFirst),
                  'snapVToSecond': int(self.snapVToSecond),
                  }

        return script

    def __str__(self):
        return '{0} >>> {1}'.format(self.source()._rawPin.getFullName(), self.destination()._rawPin.getFullName())

    def drawThick(self):
        self.pen.setWidthF(self.thickness + (self.thickness / 1.5))
        f = 0.5
        r = abs(lerp(self.color.red(), Colors.Yellow.red(), clamp(f, 0, 1)))
        g = abs(lerp(self.color.green(), Colors.Yellow.green(), clamp(f, 0, 1)))
        b = abs(lerp(self.color.blue(), Colors.Yellow.blue(), clamp(f, 0, 1)))
        self.pen.setColor(QtGui.QColor.fromRgb(r, g, b))

    def restoreThick(self):
        self.pen.setWidthF(self.thickness)
        self.pen.setColor(self.color)

    def hoverEnterEvent(self, event):
        super(UIConnection, self).hoverEnterEvent(event)
        self.drawThick()
        self.update()

    def hoverLeaveEvent(self, event):
        super(UIConnection, self).hoverLeaveEvent(event)
        self.hoverSegment = -1
        self.restoreThick()
        self.update()

    def hoverMoveEvent(self, event):
        if self.offsetting == 0:
            self.hoverSegment = -1
            if self.linPath is not None:
                tempPath = ConnectionPainter.linearPath(self.linPath)
                t = self.percentageByPoint(event.scenePos(), tempPath)
                segments = []
                for i, pos in enumerate(self.linPath[:-1]):
                    t1 = self.percentageByPoint(pos, tempPath)
                    t2 = self.percentageByPoint(self.linPath[i + 1], tempPath)
                    segments.append([t1, t2])
                for i, seg in enumerate(segments):
                    if t > seg[0] and t < seg[1]:
                        valid = []
                        if not self.sShape:
                            if self.snapVToFirst:
                                valid = [0, 1]
                            elif self.snapVToSecond:
                                valid = [1, 2]
                            else:
                                valid = [1, 2, 3]
                        else:
                            valid = [1, 2, 3]
                        if i in valid:
                            self.hoverSegment = i
                        else:
                            self.hoverSegment = -1

    def getEndPoints(self):
        p1 = self.drawSource.scenePos() + self.drawSource.pinCenter()
        if self.sourcePositionOverride is not None:
            p1 = self.sourcePositionOverride()

        p2 = self.drawDestination.scenePos() + self.drawDestination.pinCenter()
        if self.destinationPositionOverride is not None:
            p2 = self.destinationPositionOverride()

        if editableStyleSheet().ConnectionMode[0] in [ConnectionTypes.Circuit, ConnectionTypes.ComplexCircuit]:
            self.sameSide = 0
            p1n, p2n = p1, p2
            xDistance = p2.x() - p1.x()
            if self.destination().owningNode()._rawNode.__class__.__name__ in ["reroute", "rerouteExecs"]:
                if xDistance < 0:
                    p2n, p1n = p1, p2
                    self.sameSide = 1
            if self.source().owningNode()._rawNode.__class__.__name__ in ["reroute", "rerouteExecs"]:
                if xDistance < 0:
                    p1n, p2n = p1, p2
                    self.sameSide = -1
            p1, p2 = p1n, p2n
        return p1, p2

    def percentageByPoint(self, point, path, precision=0.5, width=20.0):
        percentage = -1.0
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(width)
        strokepath = stroker.createStroke(path)
        t = 0.0
        d = []
        while t <= 100.0:
            d.append(QtGui.QVector2D(point - path.pointAtPercent(t / 100)).length())
            t += precision
        percentage = d.index(min(d)) * precision
        return percentage

    def mousePressEvent(self, event):
        super(UIConnection, self).mousePressEvent(event)
        t = self.percentageByPoint(event.scenePos(), self.mPath)
        self.prevPos = event.pos()

        if abs(self.mPath.slopeAtPercent(t * 0.01)) < 1:
            self.offsetting = 1
        else:
            self.offsetting = 2

        if self.linPath is not None:
            tempPath = ConnectionPainter.linearPath(self.linPath)
            t = self.percentageByPoint(event.scenePos(), tempPath)
            segments = []
            for i, pos in enumerate(self.linPath[:-1]):
                t1 = self.percentageByPoint(pos, tempPath)
                t2 = self.percentageByPoint(self.linPath[i + 1], tempPath)
                segments.append([t1, t2])
            for i, seg in enumerate(segments):
                if t > seg[0] and t < seg[1]:
                    valid = []
                    if not self.sShape:
                        if self.snapVToFirst:
                            valid = [0, 1]
                        elif self.snapVToSecond:
                            valid = [1, 2]
                        else:
                            valid = [1, 2, 3]
                    else:
                        valid = [1, 2, 3]
                    if i in valid:
                        self.pressedSegment = i
                    else:
                        self.pressedSegment = -1
        p1, p2 = self.getEndPoints()
        offset1 = editableStyleSheet().ConnectionOffset[0]
        offset2 = -offset1
        if self.sameSide == 1:
            offset2 = offset1
        elif self.sameSide == -1:
            offset1 = offset2
        xDistance = (p2.x() + offset2) - (p1.x() + offset1)
        self.sShape = xDistance < 0
        event.accept()

    def mouseReleaseEvent(self, event):
        super(UIConnection, self).mouseReleaseEvent(event)
        self.offsetting = 0
        self.pressedSegment = -1

        event.accept()

    def mouseMoveEvent(self, event):
        super(UIConnection, self).mouseMoveEvent(event)
        if self.prevPos is not None:
            delta = self.prevPos - event.pos()
            p1, p2 = self.getEndPoints()
            if not self.sShape:
                if self.offsetting == 1:
                    doIt = True
                    if self.snapVToFirst and self.pressedSegment != 0:
                        doIt = False
                        self.pressedSegment = -1
                    elif self.snapVToSecond and self.pressedSegment != 2:
                        doIt = False
                        self.pressedSegment = -1
                    elif not self.snapVToFirst and not self.snapVToSecond:
                        if self.pressedSegment != 2:
                            doIt = False
                            self.pressedSegment = -1
                    if doIt:
                        self.vOffset -= float(delta.y())
                        if abs(self.vOffset) <= 3:
                            self.snapVToFirst = True
                            self.pressedSegment = 0
                        else:
                            self.snapVToFirst = False
                        if p1.y() + self.vOffset > p2.y() - 3 and p1.y() + self.vOffset < p2.y() + 3:
                            self.snapVToSecond = True
                            self.pressedSegment = 2
                        else:
                            self.snapVToSecond = False
                        if not self.snapVToFirst and self.pressedSegment == 0:
                            self.pressedSegment = 2

                if self.offsetting == 2:
                    if self.snapVToFirst:
                        self.hOffsetR -= float(delta.x())
                    elif self.snapVToSecond:
                        self.hOffsetL -= float(delta.x())
                    else:
                        if self.pressedSegment == 1:
                            self.hOffsetL -= float(delta.x())
                        elif self.pressedSegment == 3:
                            self.hOffsetR -= float(delta.x())
            else:
                if self.offsetting == 1 and self.pressedSegment == 2:
                    self.vOffsetSShape -= float(delta.y())
                elif self.offsetting == 2:
                    if self.pressedSegment == 1:
                        self.hOffsetRSShape -= float(delta.x())
                    elif self.pressedSegment == 3:
                        self.hOffsetLSShape -= float(delta.x())

            self.prevPos = event.pos()

        event.accept()

    def source_port_name(self):
        return self.source().getFullName()

    def shape(self):
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(10.0)
        qp.setCapStyle(QtCore.Qt.SquareCap)
        return qp.createStroke(self.path())

    def updateCurve(self, p1, p2):
        xDistance = p2.x() - p1.x()
        multiply = 3
        self.mPath = QtGui.QPainterPath()

        self.mPath.moveTo(p1)
        if xDistance < 0:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / -multiply, p1.y()),
                               QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y()), p2)
        else:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / multiply,
                                             p1.y()), QtCore.QPoint(p2.x() - xDistance / 2, p2.y()), p2)

        self.setPath(self.mPath)

    def kill(self):
        self.canvasRef().removeConnection(self)

    def paint(self, painter, option, widget):
        option.state &= ~QStyle.State_Selected

        lod = self.canvasRef().getCanvasLodValueFromCurrentScale()

        self.setPen(self.pen)
        p1, p2 = self.getEndPoints()
        roundness = editableStyleSheet().ConnectionRoundness[0]
        offset = editableStyleSheet().ConnectionOffset[0]
        offset1 = offset
        offset2 = -offset1
        if self.sameSide == 1:
            offset2 = offset1
        elif self.sameSide == -1:
            offset1 = offset2
        xDistance = (p2.x() + offset2) - (p1.x() + offset1)
        self.sShape = xDistance < 0
        sectionPath = None
        if editableStyleSheet().ConnectionMode[0] == ConnectionTypes.Circuit:
            seg = self.hoverSegment if self.hoverSegment != -1 and self.linPath and self.pressedSegment == -1 else self.pressedSegment
            self.mPath, self.linPath, sectionPath = ConnectionPainter.BasicCircuit(p1, p2, offset, roundness, self.sameSide, lod, False, self.vOffset, self.hOffsetL, self.vOffsetSShape, self.hOffsetR, self.hOffsetRSShape, self.hOffsetLSShape, self.snapVToFirst, self.snapVToSecond, seg)
        elif editableStyleSheet().ConnectionMode[0] == ConnectionTypes.ComplexCircuit:
            self.mPath, self.linPath, sectionPath = ConnectionPainter.BasicCircuit(p1, p2, offset, roundness, self.sameSide, lod, True)
        elif editableStyleSheet().ConnectionMode[0] == ConnectionTypes.Cubic:
            self.mPath = ConnectionPainter.Cubic(p1, p2, 150, lod)
            self.linPath = None
        elif editableStyleSheet().ConnectionMode[0] == ConnectionTypes.Linear:
            self.mPath, self.linPath = ConnectionPainter.Linear(p1, p2, offset, roundness, lod)
        if self.snapVToSecond and self.offsetting == 0:
            self.vOffset = p2.y() - p1.y()
        self.setPath(self.mPath)

        super(UIConnection, self).paint(painter, option, widget)
        pen = QtGui.QPen()
        pen.setColor(editableStyleSheet().MainColor)
        pen.setWidthF(self.thickness + (self.thickness / 1.5))
        painter.setPen(pen)
        if sectionPath:
            painter.drawPath(sectionPath)

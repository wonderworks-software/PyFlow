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
        self.hOffset = 0.0
        self.vOffset = 0.0
        self.ofsetting = 0
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

    @staticmethod
    def deserialize(data, graph):
        srcUUID = UUID(data['sourceUUID'])
        dstUUID = UUID(data['destinationUUID'])
        # if srcUUID in graph.pins and dstUUID in graph.pins:
        srcPin = graph.findPinByUid(srcUUID)
        assert(srcPin is not None)
        dstPin = graph.findPinByUid(dstUUID)
        assert(dstPin is not None)
        connection = graph.connectPinsInternal(srcPin, dstPin)
        assert(connection is not None)
        connection.uid = UUID(data['uuid'])
        vOffset = data['vOffset'] 
        if vOffset is not None:
            self.vOffset = float(vOffset)
        hOffset = data['hOffset'] 
        if hOffset is not None:
            self.hOffset = float(hOffset)

    def serialize(self):
        script = {'sourceUUID': str(self.source().uid),
                  'destinationUUID': str(self.destination().uid),
                  'sourceName': self.source()._rawPin.getFullName(),
                  'destinationName': self.destination()._rawPin.getFullName(),
                  'uuid': str(self.uid),
                  'vOffset':str(self.vOffset),
                  'hOffset':str(self.hOffset)
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

    def getEndPoints(self):
        p1 = self.drawSource.scenePos() + self.drawSource.pinCenter()
        if self.sourcePositionOverride is not None:
            p1 = self.sourcePositionOverride()

        p2 = self.drawDestination.scenePos() + self.drawDestination.pinCenter()
        if self.destinationPositionOverride is not None:
            p2 = self.destinationPositionOverride()
        return p1, p2

    def percentageByPoint(self, point, precision=0.5, width=20.0):
        percentage = -1.0
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(width)
        strokepath = stroker.createStroke(self.mPath) 
        if strokepath.contains(point):
            t = 0.0
            d = []
            while t <=100.0: 
                d.append(QtGui.QVector2D(point - self.mPath.pointAtPercent(t/100)).length())
                t += precision
            percentage = d.index(min(d))*precision
        return percentage

    def mousePressEvent(self, event):
        super(UIConnection, self).mousePressEvent(event)
        t = self.percentageByPoint(event.scenePos())
        self.prevPos = event.pos()
        if abs(self.mPath.slopeAtPercent(t*0.01))<1:
            self.ofsetting = 1
        else:
            self.ofsetting = 2
        event.accept()

    def mouseReleaseEvent(self, event):
        super(UIConnection, self).mouseReleaseEvent(event)
        self.ofsetting = 0
        event.accept()

    def mouseMoveEvent(self, event):
        super(UIConnection, self).mouseMoveEvent(event)
        delta = self.prevPos-event.pos()
        delta /= self.canvasRef().currentViewScale()
        if self.ofsetting == 1:
            self.vOffset -= float(delta.y())
        elif self.ofsetting == 2:
            self.hOffset -= float(delta.x())
        self.prevPos = event.pos()
        event.accept()

    def hoverLeaveEvent(self, event):
        super(UIConnection, self).hoverLeaveEvent(event)
        self.restoreThick()
        self.update()

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
        if editableStyleSheet().ConnectionMode[0] in [ConnectionTypes.Circuit, ConnectionTypes.ComplexCircuit]:
            sameSide = 0
            offset = 20.0
            roundnes = editableStyleSheet().ConnectionRoundness[0]
            if self.destination().owningNode()._rawNode.__class__.__name__ in ["reroute", "rerouteExecs"]:
                xDistance = p2.x() - p1.x()
                if xDistance < 0:
                    p2, p1 = self.getEndPoints()
                    sameSide = 1
            if self.source().owningNode()._rawNode.__class__.__name__ in ["reroute", "rerouteExecs"]:
                p11, p22 = self.getEndPoints()
                xDistance = p22.x() - p11.x()
                if xDistance < 0:
                    sameSide = -1
                    p1, p2 = self.getEndPoints()
            self.mPath = ConnectionPainter.BasicCircuit(p1, p2, offset, roundnes, sameSide, lod, editableStyleSheet().ConnectionMode[0]==ConnectionTypes.ComplexCircuit,self.vOffset,self.hOffset)

        elif editableStyleSheet().ConnectionMode[0] == ConnectionTypes.Cubic:
            self.mPath = ConnectionPainter.Cubic(p1, p2, 150, lod)

        self.setPath(self.mPath)

        super(UIConnection, self).paint(painter, option, widget)

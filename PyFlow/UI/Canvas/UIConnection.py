import weakref
from uuid import UUID, uuid4

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsPathItem
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QStyle

from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.UICommon import NodeDefaults
from PyFlow.Core.Common import *


# UIConnection between pins
class UIConnection(QGraphicsPathItem):
    """UIConnection is a cubic spline curve. It represents connecton between two pins.
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

        if self.drawSource._rawPin.isExec() or self.drawDestination._rawPin.isExec():
            if self.thickness != 2:
                self.thickness = 2
                self.pen.setWidthF(self.thickness)
                self.update()

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

    def serialize(self):
        script = {'sourceUUID': str(self.source().uid),
                  'destinationUUID': str(self.destination().uid),
                  'sourceName': self.source()._rawPin.getFullName(),
                  'destinationName': self.destination()._rawPin.getFullName(),
                  'uuid': str(self.uid)
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

    def mousePressEvent(self, event):
        super(UIConnection, self).mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(UIConnection, self).mouseReleaseEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        super(UIConnection, self).mouseMoveEvent(event)
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

        lod = self.canvasRef().getLodValueFromCurrentScale(5)

        self.setPen(self.pen)
        p1, p2 = self.getEndPoints()

        if lod >= 5:
            self.mPath = QtGui.QPainterPath()
            self.mPath.moveTo(p1)
            self.mPath.lineTo(p2)
        else:
            xDistance = p2.x() - p1.x()
            vDistance = p2.y() - p1.y()
            offset = abs(xDistance) * 0.5
            defOffset = 150
            if abs(xDistance) < defOffset:
                offset = defOffset / 2
            if abs(vDistance) < 20:
                offset = abs(xDistance) * 0.3
            multiply = 2
            self.mPath = QtGui.QPainterPath()
            self.mPath.moveTo(p1)
            if xDistance < 0:
                self.cp1 = QtCore.QPoint(p1.x() + offset, p1.y())
                self.cp2 = QtCore.QPoint(p2.x() - offset, p2.y())
            else:
                self.cp2 = QtCore.QPoint(p2.x() - offset, p2.y())
                self.cp1 = QtCore.QPoint(p1.x() + offset, p1.y())
            self.mPath.cubicTo(self.cp1, self.cp2, p2)

        self.setPath(self.mPath)
        super(UIConnection, self).paint(painter, option, widget)

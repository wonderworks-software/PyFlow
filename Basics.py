import sys
import weakref
import math
from PySide import QtCore, QtGui


class PortTypes:

    kInput = 'input'
    kOutput = 'output'


class Spacings:
    kPortSpacing = 4
    kPortOffset = 12


class Colors(object):

    kNodeBackgrounds = QtGui.QColor(45, 45, 45, 100)
    kConnectors = QtGui.QColor(0, 100, 0, 255)
    kPortLinesA = QtGui.QColor(0, 90, 0, 50)
    kPortLinesB = QtGui.QColor(0, 0, 90, 50)
    kNodeNameRect = QtGui.QColor(100, 100, 100, 100)
    kRed = QtGui.QColor(255, 0, 0, 255)
    kGreen = QtGui.QColor(0, 255, 0, 255)
    kBlue = QtGui.QColor(0, 0, 255, 255)
    kBlack = QtGui.QColor(255, 255, 255, 255)

    def __init__(self):
        super(Colors, self).__init__()


class EllipseWidget(QtGui.QGraphicsWidget, Colors):

    def __init__(self, name, width, height, color=Colors.kConnectors):

        QtGui.QGraphicsWidget.__init__(self)
        self.setAcceptHoverEvents(True)
        self.color = color
        self.name = name
        self.__width = width+1
        self.__height = height+1
        self.hovered = False

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):

        bgRect = self.boundingRect()
        if self.hovered:
            painter.setBrush(QtGui.QBrush(self.color.lighter(160)))
        else:
            painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(bgRect)


    def mousePressEvent(self, *args, **kwargs):

        print self.name, 'pressed'

    def mouseReleaseEvent(self, *args, **kwargs):

        print self.name, 'released'

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False


class Edge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.arrowSize = 10.0
        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source()

    def setSourceNode(self, node):
        self.source = weakref.ref(node)
        self.adjust()

    def destNode(self):
        return self.dest()

    def setDestNode(self, node):
        self.dest = weakref.ref(node)
        self.adjust()

    def adjust(self):
        if not self.source() or not self.dest():
            return

        line = QtCore.QLineF(self.mapFromItem(self.source(), 0, 0), self.mapFromItem(self.dest(), 0, 0))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
                                                          math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize);
        destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                                      math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class NodeName(QtGui.QGraphicsTextItem, Colors):
    def __init__(self, Name, parent):
        QtGui.QGraphicsTextItem.__init__(self)
        self.setPlainText(Name)
        self.setParentItem(parent)
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setPos(parent.sizes[0], parent.sizes[1]-self.boundingRect().height())

    def keyPressEvent(self, event):
        key = event.key()
        if (key == QtCore.Qt.Key_Return) or (key == QtCore.Qt.Key_Escape):
            self.setEnabled(False)
            self.setEnabled(True)
            return
        else:
            QtGui.QGraphicsTextItem.keyPressEvent(self, event)

    def paint(self, painter, option, widget):
        # paint the background
        painter.fillRect(option.rect, QtGui.QColor(self.kNodeNameRect))

        # paint the normal TextItem with the default 'paint' method
        super(NodeName, self).paint(painter, option, widget)


class ConnectorItem(QtGui.QGraphicsWidget):

    Type = QtGui.QGraphicsWidget.UserType + 1

    def __init__(self, i_type):
        QtGui.QGraphicsWidget.__init__(self)

        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        # self.setZValue(-1)
        self.size = [0.0, 0.0, 15.0, 15.0, 5.0, 5.0]

    def type(self):

        return ConnectorItem.Type

    def addEdge(self, edge):

        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    def edges(self):

        return self.edgeList

    def calculateForces(self):

        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.newPos = self.pos()
            return

    def advance(self):

        if self.newPos == self.pos():
            return False

        self.setPos(self.newPos)
        return True

    def boundingRect(self):

        penWidth = 1.0
        return QtCore.QRectF(self.size[0] - penWidth / 2, self.size[1] - penWidth / 2,
                      self.size[2] + penWidth, self.size[3] + penWidth)

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(self.boundingRect())

        gradient = QtGui.QColor(0, 90, 0, 90)
        if option.state & QtGui.QStyle.State_Sunken:
            gradient = gradient.lighter(160)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(self.boundingRect())

    def itemChange(self, change, value):

        if change == QtGui.QGraphicsWidget.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()
            # self.graph().itemMoved()

        return QtGui.QGraphicsWidget.itemChange(self, change, value)

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.update()
        QtGui.QGraphicsWidget.mouseReleaseEvent(self, event)


class Node(QtGui.QGraphicsItem, Colors):
    def __init__(self, Name, graphWidget, w, h):
        self.color = 1
        QtGui.QGraphicsItem.__init__(self)
        self.inputs = []
        self.outputs = []
        self.w = w
        self.h = h
        self.graph = graphWidget
        self.setFlag(self.ItemIsMovable)
        self.sizes = [0, 0, self.w, self.h, 2, 2]
        # set node name
        self.label = NodeName(Name, self)
        # set node layout
        self.v_form = QtGui.QGraphicsWidget()
        self.v_form.setMaximumWidth(self.boundingRect().width()+Spacings.kPortOffset)
        self.v_form.setGeometry(QtCore.QRectF(0, 0, self.w+Spacings.kPortOffset, self.h))
        self.v_form.setParentItem(self)
        # self.v_form.setAutoFillBackground(True)
        self.layout = QtGui.QGraphicsLinearLayout()
        self.layout.setOrientation(QtCore.Qt.Vertical)
        self.layout.setSpacing(Spacings.kPortSpacing)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.v_form.setLayout(self.layout)
        self.v_form.setX(self.v_form.x()-Spacings.kPortOffset/2)
        self.add_port(PortTypes.kInput, 'in')
        self.add_port(PortTypes.kOutput, 'out')


    def boundingRect(self):

        penWidth = 1.0
        return QtCore.QRectF(self.sizes[0] - penWidth / 2, self.sizes[1] - penWidth / 2,
                             self.sizes[2] + penWidth, self.v_form.boundingRect().bottomRight().y() + penWidth + 3)

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+3,
                                self.sizes[4], self.sizes[5])

        color = self.kNodeBackgrounds
        if option.state & QtGui.QStyle.State_Sunken:
            color = color.lighter(160)

        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+3,
                                self.sizes[4], self.sizes[5])

    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)
        print 'inputs', [i.name for i in self.inputs]
        print 'outputs', [i.name for i in self.outputs]

    def mouseReleaseEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)

    def add_port(self, Type, name, color=Colors.kConnectors):

        cn = EllipseWidget(name, 10, 10, color)
        connector_name = QtGui.QGraphicsProxyWidget()
        lbl = QtGui.QLabel(name)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        connector_name.setWidget(lbl)
        lyt = QtGui.QGraphicsLinearLayout()
        form = QtGui.QGraphicsWidget()
        # set color
        palette = form.palette()
        if self.color > 0:
            palette.setColor(palette.Window, Colors.kPortLinesA)
            self.color *= -1
        else:
            palette.setColor(palette.Window, Colors.kPortLinesB)
            self.color *= -1
        form.setPalette(palette)

        lyt.setSpacing(Spacings.kPortSpacing)
        if Type == PortTypes.kInput:
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lyt.addItem(cn)
            lyt.addItem(connector_name)
            self.inputs.append(cn)
        elif Type == PortTypes.kOutput:
            lbl.setAlignment(QtCore.Qt.AlignRight)
            lyt.addItem(connector_name)
            lyt.addItem(cn)
            self.outputs.append(cn)
        lyt.setContentsMargins(1, 1, 1, 1)
        lyt.setMaximumHeight(Spacings.kPortOffset)
        form.setLayout(lyt)
        form.setZValue(1)
        form.setAutoFillBackground(True)
        form.setGeometry(QtCore.QRectF(0, 0, self.w+Spacings.kPortOffset+3, self.h))
        self.layout.addItem(form)


class GraphWidget(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)

        self.timerId = 0

        self.scene_widget = QtGui.QGraphicsScene(self)
        self.scene_widget.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene_widget.setSceneRect(-200, -200, 400, 400)
        self.setScene(self.scene_widget)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(self.tr("Elastic Nodes"))

    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Plus:
            self.scaleView(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scaleView(1 / 1.2)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, ConnectorItem):
                    item.setPos(-150 + QtCore.qrand() % 300, -150 + QtCore.qrand() % 300)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)


    def timerEvent(self, event):
        nodes = [item for item in self.scene().items() if isinstance(item, ConnectorItem)]

        for node in nodes:
            node.calculateForces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):
        # Shadow.
        sceneRect = self.sceneRect()
        # Fill.
        gradient = QtGui.QColor(65, 65, 65)
        painter.fillRect(rect.intersect(sceneRect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(sceneRect)

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

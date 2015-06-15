import sys
import weakref
import math
from PySide import QtCore, QtGui


class PortTypes(object):

    kInput = 'input'
    kOutput = 'output'

    def __init__(self):
        super(PortTypes, self).__init__()


class Spacings(object):

    kPortSpacing = 4
    kPortOffset = 12

    def __init__(self):
        super(Spacings, self).__init__()


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
    kConnectionLines = QtGui.QColor(255, 255, 255, 90)

    def __init__(self):
        super(Colors, self).__init__()


class EllipseWidget(QtGui.QGraphicsWidget, Colors):

    def __init__(self, name, width, height, color=Colors.kConnectors):

        QtGui.QGraphicsWidget.__init__(self)
        self.edgeList = []
        self.port_type = None
        self.owned_node = None
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

        self.setAcceptHoverEvents(True)
        self.color = color
        self.name = name
        self.__width = width+1
        self.__height = height+1
        self.hovered = False

        self.startPos = None
        self.endPos = None

    def add_edge(self, edge):

        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    def edges(self):

        return self.edgeList

    def calculate_forces(self):

        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.newPos = self.pos()
            return

    def advance(self):

        if self.newPos == self.pos():
            return False

        self.setPos(self.newPos)
        return True

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):

        background_rect = self.boundingRect()
        if self.hovered:
            painter.setBrush(QtGui.QBrush(self.color.lighter(160)))
        else:
            painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(background_rect)

    def mousePressEvent(self, event):

        for i in self.edgeList:
            print i.toolTip()

    def mouseReleaseEvent(self, event):

        target = self.scene().views()[0].last_cursor_item
        if not target:
            return
        if target.port_type == self.port_type:
            print 'same types can not be connected'
            return
        edge = Edge(self, target)
        self.scene().addItem(edge)
        self.edgeList.append(edge)
        target.edgeList.append(edge)

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False


class Edge(QtGui.QGraphicsItem, Colors):

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, source_node, dest_node):
        QtGui.QGraphicsItem.__init__(self)
        self.arrow_size = 10.0
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = source_node
        self.dest = dest_node
        self.setZValue(-1)
        self.connection = {'From': self.source.owned_node.name+'|'+self.source.name,
                           'To': self.dest.owned_node.name+'|'+self.dest.name}
        self.setToolTip(self.connection['From']+'>>>'+self.connection['To'])

    def paint(self, painter, option, widget):

        painter.setPen(QtGui.QPen(self.kConnectionLines, 3, QtCore.Qt.DashDotLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        offset = self.source.boundingRect().width()/2
        x1 = self.source.scenePos().x()+offset
        x2 = self.dest.scenePos().x()+offset
        y1 = self.source.scenePos().y()+offset
        y2 = self.dest.scenePos().y()+offset
        # path = QtGui.QPainterPath()
        # path.moveTo(self.source.scenePos().x()+offset, self.source.scenePos().y()+offset)
        # mid = QtCore.QPointF(((x1+x2)/2), ((y1+y2)/2))
        # c_offset = 50
        # mult = y1/y2
        # if y1 > y2:
        #     ctrl1 = QtCore.QPointF(mid.x(), mid.y()+c_offset*mult)
        #     ctrl2 = QtCore.QPointF(mid.x(), mid.y()-c_offset*mult)
        # elif y1 < y2:
        #     ctrl1 = QtCore.QPointF(mid.x(), mid.y()-c_offset*mult)
        #     ctrl2 = QtCore.QPointF(mid.x(), mid.y()+c_offset*mult)
        # path.cubicTo(ctrl1, ctrl2, QtCore.QPointF(self.dest.scenePos().x()+offset, self.dest.scenePos().y()+offset))
        # painter.drawPath(path)
        painter.drawLine(x1, y1, x2, y2)

    def boundingRect(self):

        return QtCore.QRectF()


class NodeName(QtGui.QGraphicsTextItem, Colors):
    def __init__(self, name, parent):
        QtGui.QGraphicsTextItem.__init__(self)
        self.name = name
        self.setPlainText(self.name)
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


class Node(QtGui.QGraphicsItem, Colors):
    def __init__(self, name, graph_widget, w, h):
        self.color = 1
        QtGui.QGraphicsItem.__init__(self)
        self.inputs = []
        self.outputs = []
        self.w = w
        self.h = h
        self.graph = graph_widget
        self.setFlag(self.ItemIsMovable)
        self.sizes = [0, 0, self.w, self.h, 2, 2]
        # set node name
        self.name = name
        self.label = NodeName(self.name, self)
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

        pen_width = 1.0
        return QtCore.QRectF(self.sizes[0] - pen_width / 2, self.sizes[1] - pen_width / 2,
                             self.sizes[2] + pen_width, self.v_form.boundingRect().bottomRight().y() + pen_width + 3)

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

    def add_port(self, port_type, name, color=QtGui.QColor(0, 100, 0, 255)):

        cn = EllipseWidget(name, 10, 10, color)
        cn.port_type = port_type
        cn.owned_node = self
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
        if port_type == PortTypes.kInput:
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lyt.addItem(cn)
            lyt.addItem(connector_name)
            self.inputs.append(cn)
        elif port_type == PortTypes.kOutput:
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

        self.last_cursor_item = None
        self._isPanning = False
        self._mousePressed = False
        self.timerId = 0
        self.setViewportUpdateMode(self.FullViewportUpdate)

        self.scene_widget = QtGui.QGraphicsScene(self)
        self.scene_widget.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene_widget.setSceneRect(-400, -400, 800, 800)
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
            self.scale_view(1.2)
        elif key == QtCore.Qt.Key_Minus:
            self.scale_view(1 / 1.2)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            for item in self.scene().items():
                if isinstance(item, ConnectorItem):
                    item.setPos(-150 + QtCore.qrand() % 300, -150 + QtCore.qrand() % 300)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

    def mousePressEvent(self,  event):

        if event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        super(GraphWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        self.setDragMode(QtGui.QGraphicsView.NoDrag)
        self.last_cursor_item = self.itemAt(event.pos())
        super(GraphWidget, self).mouseReleaseEvent(event)

    def timerEvent(self, event):

        nodes = [item for item in self.scene().items() if isinstance(item, ConnectorItem)]

        for node in nodes:
            node.calculate_forces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):

        self.scale_view(math.pow(2.0, event.delta() / 240.0))

    def drawBackground(self, painter, rect):

        # Shadow.
        scene_rect = self.sceneRect()
        # Fill.
        gradient = QtGui.QColor(65, 65, 65)
        painter.fillRect(rect.intersect(scene_rect), QtGui.QBrush(gradient))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(scene_rect)

    def scale_view(self, scale_factor):

        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scale_factor, scale_factor)

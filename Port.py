from PySide import QtCore
from PySide import QtGui
from Settings import *
import weakref
from Edge import Edge


class Port(QtGui.QGraphicsWidget, Colors):

    def __init__(self, name, width, height, color=Colors.kConnectors):

        QtGui.QGraphicsWidget.__init__(self)
        self.edgeList = []
        self.port_type = None
        self.owned_node = None
        self.setZValue(1)
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

        pass

    def mouseReleaseEvent(self, event):

        target = self.scene().views()[0].last_cursor_item
        if not hasattr(target, 'port_type'):
            print 'this is not a connector'
            return
        if target.port_type == self.port_type:
            print 'same types can not be connected'
            return
        From = ''.join([self.owned_node.label.name, '.', self.name])
        To = ''.join([target.owned_node.label.name, '.', target.name])
        if self.port_type == PortTypes.kOutput:
            connection = {'From': From, 'To': To}
            target_node_connections = target.owned_node.get_input_edges()
        else:
            connection = {'From': To, 'To': From}
            target_node_connections = self.owned_node.get_input_edges()
        print 'THIS CONNECTION ', connection
        for i in target_node_connections.itervalues():
            for c in i:
                if c['From'] == connection['From'] and c['To'] == connection['To']:
                    print connection, 'already connected'
                    return

        if self.port_type == PortTypes.kOutput:
            edge = Edge(self, target)
        else:
            edge = Edge(target, self)
        self.scene().addItem(edge)
        self.edgeList.append(edge)
        target.edgeList.append(edge)
        edge.connection = connection

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

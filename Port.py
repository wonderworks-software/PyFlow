from PySide import QtCore
from PySide import QtGui
from Settings import *
import weakref
from Edge import Edge


class Port(QtGui.QGraphicsWidget):

    def __init__(self, name, width, height, color=Colors.kConnectors):

        QtGui.QGraphicsWidget.__init__(self)
        self.Type = 'PORT'
        self.menu = QtGui.QMenu()

        self.disconnected = self.menu.addAction('Disconnect all')
        self.disconnected.triggered.connect(self.disconnect_all)

        # this list holds Edge objects
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

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def connection_name(self):

        return self.owned_node.name+'.'+self.name

    def get_destination_connected_ports(self):

        return [i.destination for i in self.edgeList]

    def get_source_connected_ports(self):

        return [i.source for i in self.edgeList]

    def disconnect_all(self):

        if self.port_type == PortTypes.kOutput:
            for i in self.get_destination_connected_ports():
                for e in self.edgeList:
                    if e in i.edgeList:
                        i.edgeList.remove(e)
            [self.scene().removeItem(i) for i in self.scene().items() if i in self.edgeList]
        else:
            for i in self.get_source_connected_ports():
                for e in self.edgeList:
                    if e in i.edgeList:
                        i.edgeList.remove(e)
            [self.scene().removeItem(i) for i in self.scene().items() if i in self.edgeList]
        self.edgeList = []
        self.disconnected_user_function()

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

    def disconnected_user_function(self):

        print 'DISCONNECTED CODE'

    def connected_user_function(self):

        print 'SUCCESS CONNECTION CODE'

    def contextMenuEvent(self, event):

        self.menu.exec_(event.screenPos())

    def mouseReleaseEvent(self, event):

        target = self.scene().views()[0].last_cursor_item
        # check if dropped item is Port
        if not hasattr(target, 'port_type'):
            print 'this is not a connector'
            return
        # check if it is not self
        if self.owned_node.name == target.owned_node.name:
            print 'can not connect to self'
            return
        # check if it is not same port type
        if target.port_type == self.port_type:
            print 'same types can not be connected'
            return
        connection_from = ''.join([self.owned_node.label.name, '.', self.name])
        connection_to = ''.join([target.owned_node.label.name, '.', target.name])
        if self.port_type == PortTypes.kOutput:
            connection = {'From': connection_from, 'To': connection_to}
            target_node_connections = target.owned_node.get_input_edges()
        else:
            connection = {'From': connection_to, 'To': connection_from}
            target_node_connections = self.owned_node.get_input_edges()
        # check if this connection already exists
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
        self.connected_user_function()

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

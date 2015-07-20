from PySide import QtCore
from PySide import QtGui
from Settings import *
from AbstractGraph import *
from Settings import *


class Port(QtGui.QGraphicsWidget, AGPort):

    def __init__(self, name, parent, width, height, color=Colors.kConnectors):

        QtGui.QGraphicsWidget.__init__(self)
        AGPort.__init__(self, name, parent)
        # self.object_type = AGObjectTypes.tPort
        # self.type = None
        # self.parent = parent
        self.menu = QtGui.QMenu()

        self.disconnected = self.menu.addAction('Disconnect all')
        self.get_data_action = self.menu.addAction('GET_DATA')
        self.plot_action = self.menu.addAction('PLOT')
        self.disconnected.triggered.connect(self.disconnect_all)
        self.get_data_action.triggered.connect(self.get_data)
        self.plot_action.triggered.connect(self.parent.graph.plot)

        # this list holds Edge objects
        # self.edge_list = []

        # self.type = None
        # self.parent = parent
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)

        self.setAcceptHoverEvents(True)
        self.color = color
        # self.name = name
        self.__width = width+1
        self.__height = height+1
        self.hovered = False

        self.startPos = None
        self.endPos = None
        self._dirty_pen = QtGui.QPen(Colors.kDirtyPen, 1, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def connection_name(self):

        return self.parent.name+'.'+self.name

    def get_destination_connected_ports(self):

        return [i.destination for i in self.edge_list]

    def get_source_connected_ports(self):

        return [i.source for i in self.edge_list]

    def disconnect_all(self):

        if self.type == AGPortTypes.kOutput:
            for i in self.get_destination_connected_ports():
                for e in self.edge_list:
                    if e in i.edge_list:
                        i.edge_list.remove(e)
                        print e, [i for i in self.parent.graph.edges]
            [self.scene().removeItem(i) for i in self.scene().items() if i in self.edge_list]
        else:
            for i in self.get_source_connected_ports():
                for e in self.edge_list:
                    if e in i.edge_list:
                        i.edge_list.remove(e)
                        print e, [i for i in self.parent.graph.edges]
            [self.scene().removeItem(i) for i in self.scene().items() if i in self.edge_list]
        self.edge_list = []

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):

        background_rect = self.boundingRect()
        if self.dirty:
            painter.setPen(self._dirty_pen)
        if self.hovered:
            painter.setBrush(QtGui.QBrush(self.color.lighter(160)))
        else:
            painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(background_rect)

    def mousePressEvent(self, event):

        pass

    def contextMenuEvent(self, event):

        self.menu.exec_(event.screenPos())

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True
        if self.parent.graph.is_debug():
            print 'data -', self._data

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

    def get_data(self):

        debug = self.parent.graph.is_debug()
        if self.type == AGPortTypes.kOutput:
            if self.dirty:
                compute_order = self.parent.graph.get_evaluation_order(self.parent)
                for i in reversed(sorted([i for i in compute_order.keys()])):
                    if not self.parent.graph.is_multithreaded():
                        for n in compute_order[i]:
                            if debug:
                                print n.name, 'calling compute'
                            n.compute()
                            n.update_ports()
                    else:
                        if debug:
                            print 'multithreaded calc of layer', [n.name for n in compute_order[i]]
                        calc_multithreaded(compute_order[i], debug)
                        [i.update_ports() for i in compute_order[i]]
                self.dirty = False
                return self._data
            else:
                return self._data
        if self.type == AGPortTypes.kInput:
            if self.dirty:
                out = [i for i in self.affected_by if i.type == AGPortTypes.kOutput]
                if not out == []:
                    compute_order = out[0].parent.graph.get_evaluation_order(out[0].parent)
                    for i in reversed(sorted([i for i in compute_order.keys()])):
                        if not self.parent.graph.is_multithreaded():
                            for n in compute_order[i]:
                                if debug:
                                    print n.name, 'calling compute'
                                n.compute()
                                n.update_ports()
                        else:
                            if debug:
                                print 'multithreaded calc of layer', [n.name for n in compute_order[i]]
                            calc_multithreaded(compute_order[i], debug)
                            [i.update_ports() for i in compute_order[i]]
                    self.dirty = False
                    out[0].dirty = False
                    return out[0]._data
            else:
                return self._data
        else:
            return self._data

    def set_data(self, data, dirty_propagate=True):

        self._data = data
        self.set_clean()
        if self.type == AGPortTypes.kOutput:
            for i in self.affects:
                i._data = data
                i.set_clean()
        if dirty_propagate:
            push(self, True)

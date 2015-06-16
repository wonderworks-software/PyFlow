from Settings import *
from PySide import QtGui
from PySide import QtCore
from Port import EllipseWidget


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
        # print 'inputs', [i.name for i in self.inputs]
        # print 'outputs', [i.name for i in self.outputs]
        print 'inputs'
        for i in [i.edgeList for i in self.inputs]:
            if not i.__len__() == 0:
                print i
        print 'outputs'
        for i in [i.edgeList for i in self.outputs]:
            if not i.__len__() == 0:
                print i

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

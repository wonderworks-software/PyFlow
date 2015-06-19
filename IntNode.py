import BaseNode
from Settings import *
from Port import *
from PySide import QtCore


class IntNode(BaseNode.Node):
    def __init__(self, name, graph_widget):
        super(IntNode, self).__init__(name, graph_widget, w=120, colors=Colors, spacings=Spacings, port_types=PortTypes)
        self.data = 5
        self.port_types = PortTypes
        self.spacings = Spacings
        # self.height_offset = 15
        self.colors = Colors
        self.add_port(self.port_types.kOutput, 'out', self.colors.kInteger)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

        color = self.colors.kNodeBackgrounds
        if option.state & QtGui.QStyle.State_Sunken:
            color = color.lighter(160)

        painter.setBrush(QtGui.QBrush(self.colors.kIntNodeBackground))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

    def get_data(self):

        return self.data

    def add_port(self, port_type, name, color=QtGui.QColor(0, 100, 0, 255)):

        cn = Port(name, 10, 10, color)
        cn.port_type = port_type
        cn.owned_node = self
        connector_name = QtGui.QGraphicsProxyWidget()
        spin_box_proxy = QtGui.QGraphicsProxyWidget()
        spin_box_proxy.setScale(0.5)
        lbl = QtGui.QLabel(name)
        spin_box = QtGui.QSpinBox()
        spin_box.setMaximum(999999999)
        spin_box.setMinimum(-999999999)
        spin_box.setAlignment(QtCore.Qt.AlignRight)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        connector_name.setWidget(lbl)
        spin_box_proxy.setWidget(spin_box)
        lyt = QtGui.QGraphicsLinearLayout()
        form = QtGui.QGraphicsWidget()
        # set color
        palette = form.palette()
        if self.color_idx > 0:
            palette.setColor(palette.Window, self.colors.kPortLinesA)
            self.color_idx *= -1
        else:
            palette.setColor(palette.Window, self.colors.kPortLinesB)
            self.color_idx *= -1
        form.setPalette(palette)

        lyt.setSpacing(self.spacings.kPortSpacing)
        if port_type == self.port_types.kInput:
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lyt.addItem(cn)
            lyt.addItem(connector_name)
            lyt.addItem(spin_box_proxy)
            self.inputs.append(cn)
        elif port_type == self.port_types.kOutput:
            lbl.setAlignment(QtCore.Qt.AlignRight)
            lyt.addItem(spin_box_proxy)
            lyt.addItem(connector_name)
            lyt.addItem(cn)
            self.outputs.append(cn)
        lyt.setContentsMargins(1, 1, 1, 1)
        lyt.setMaximumHeight(self.spacings.kPortOffset)
        form.setLayout(lyt)
        form.setZValue(1)
        form.setAutoFillBackground(True)
        form.setGeometry(QtCore.QRectF(0, 0, self.w+self.spacings.kPortOffset+3, self.h))
        self.layout.addItem(form)

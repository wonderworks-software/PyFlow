import BaseNode
from Port import *
from PySide import QtCore
from AbstractGraph import *


class SBox(QtGui.QSpinBox):
    def __init__(self, foo):
        super(SBox, self).__init__()
        self.foo = foo
        self.valueChanged.connect(self.foo)


class IntNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(IntNode, self).__init__(name, graph, w=120, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.spin_box = SBox(self.set_data)
        self.graph = graph
        self.spacings = Spacings
        # self.height_offset = 15
        self.colors = Colors
        self.output = self._add_port(AGPortTypes.kOutput, AGPortDataTypes.tNumeric, 'out')
        self.compute()

    def paint(self, painter, option, widget):

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

        color = self.colors.kInteger
        if self.isSelected():
            color = color.lighter(160)

        painter.setBrush(QtGui.QBrush(color))
        pen = QtGui.QPen(QtCore.Qt.black, 0)
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(Colors.kWhite)
            pen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(pen)
        painter.drawRoundedRect(self.sizes[0], self.sizes[1],
                                self.sizes[2], self.v_form.boundingRect().bottomRight().y()+self.height_offset,
                                self.sizes[4], self.sizes[5])

    def _add_port(self, port_type, data_type, name, color=QtGui.QColor(0, 100, 0, 255)):

        cn = Port(name, self, data_type, 10, 10, color)
        cn.type = port_type
        cn.parent = self
        connector_name = QtGui.QGraphicsProxyWidget()
        spin_box_proxy = QtGui.QGraphicsProxyWidget()
        spin_box_proxy.setScale(0.5)
        lbl = QtGui.QLabel(name)
        self.spin_box.setMaximum(999999999)
        self.spin_box.setMinimum(-999999999)
        self.spin_box.setAlignment(QtCore.Qt.AlignRight)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        connector_name.setWidget(lbl)
        spin_box_proxy.setWidget(self.spin_box)
        lyt = QtGui.QGraphicsLinearLayout()
        form = QtGui.QGraphicsWidget()
        # set color
        palette = form.palette()
        if self._color_idx > 0:
            palette.setColor(palette.Window, self.colors.kPortLinesA)
            self._color_idx *= -1
        else:
            palette.setColor(palette.Window, self.colors.kPortLinesB)
            self._color_idx *= -1
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
        # form.setZValue(1)
        form.setAutoFillBackground(True)
        form.setGeometry(QtCore.QRectF(0, 0, self.w+self.spacings.kPortOffset+3, self.h))
        self.layout.addItem(form)
        return cn

    def set_data(self):

        self.output.set_data(self.spin_box.value(), True)

    def compute(self):

        self.output.set_data(self.spin_box.value(), False)

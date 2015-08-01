from AGraphPySide.Port import *
from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class DSBox(QtGui.QDoubleSpinBox):
    def __init__(self, foo):
        super(DSBox, self).__init__()
        self.foo = foo
        self.valueChanged.connect(self.foo)


class FloatNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(FloatNode, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.spin_box = DSBox(self.set_data)
        self.graph = graph
        self.layout.setSpacing(3)
        self.height_offset = 13
        self.colors = Colors()
        self.colors.kNodeBackgrounds = QtGui.QColor(45, 45, 95, 120)
        self.output = self._add_port(AGPortTypes.kOutput, AGPortDataTypes.tNumeric, 'out')
        self.compute()

    def _add_port(self, port_type, data_type, name, color=QtGui.QColor(0, 100, 0, 255)):

        cn = Port(name, self, data_type, 10, 10, color)
        cn.allowed_data_types = [data_type]
        cn.type = port_type
        cn.parent = self
        connector_name = QtGui.QGraphicsProxyWidget()
        spin_box_proxy = QtGui.QGraphicsProxyWidget()

        lbl = QtGui.QLabel(name)
        self.spin_box.setMaximum(999999999)
        self.spin_box.setMinimum(-999999999)
        self.spin_box.setAlignment(QtCore.Qt.AlignRight)
        lbl.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        connector_name.setWidget(lbl)
        spin_box_proxy.setWidget(self.spin_box)
        lyt = self.add_layout()
        lyt_head = self.add_layout()
        # lyt.addItem(spin_box_proxy)
        lyt_head.addItem(spin_box_proxy)

        if port_type == self.port_types.kInput:
            lbl.setAlignment(QtCore.Qt.AlignLeft)
            lyt.addItem(cn)
            lyt.addItem(connector_name)
            # lyt.addItem(spin_box_proxy)
            self.inputs.append(cn)
        elif port_type == self.port_types.kOutput:
            lbl.setAlignment(QtCore.Qt.AlignRight)
            # lyt.addItem(spin_box_proxy)
            lyt.addItem(connector_name)
            lyt.addItem(cn)
            self.outputs.append(cn)
        return cn

    def set_data(self):

        self.output.set_data(self.spin_box.value(), True)

    def compute(self):

        self.output.set_data(self.spin_box.value(), False)

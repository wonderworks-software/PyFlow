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
        lyt_head = self.add_layout()
        spin_box_proxy = QtGui.QGraphicsProxyWidget()
        spin_box_proxy.setWidget(self.spin_box)
        lyt_head.addItem(spin_box_proxy)
        self.compute()    

    def set_data(self):

        self.output.set_data(self.spin_box.value(), True)

    def compute(self):

        self.output.set_data(self.spin_box.value(), False)

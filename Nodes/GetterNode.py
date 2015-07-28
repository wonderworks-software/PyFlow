from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class GetterNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph, colors=Colors):
        super(GetterNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.input = self.add_input_port('input', AGPortDataTypes.tAny)
        self.colors = colors
        # add request button
        lyt = self.add_layout()
        pb = QtGui.QPushButton('request')
        prx_btn = QtGui.QGraphicsProxyWidget()
        prx_btn.setWidget(pb)
        lyt.addItem(prx_btn)
        lyt.setAlignment(lyt.itemAt(0), QtCore.Qt.AlignCenter)

        pb.clicked.connect(self.compute)

    def compute(self):

        if self.input.dirty:
            data = self.input.get_data()
            print(str(data))
        else:
            print(str(self.input.current_data()))

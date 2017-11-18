from PySide import QtCore
from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class Call(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Call, self).__init__(name, graph)
        self.out = self.add_output_port("OUT", AGPortDataTypes.tExec, self.compute)
        pb = QtGui.QPushButton('request')
        con = self.add_container(AGPortTypes.kOutput)

        pb.clicked.connect(self.compute)
        prx_btn = QtGui.QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        con.layout().addItem(prx_btn)

    @staticmethod
    def get_category():
        return 'Util'

    def compute(self):
        self.out.call()

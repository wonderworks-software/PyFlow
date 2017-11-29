from Qt import QtCore
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from AbstractGraph import *
from Settings import *
from Node import Node


class Call(Node, NodeBase):
    def __init__(self, name, graph):
        super(Call, self).__init__(name, graph)
        self.out = self.add_output_port("OUT", DataTypes.Exec, self.compute)
        pb = QPushButton('request')
        con = self.add_container(PinTypes.Output)

        pb.clicked.connect(self.compute)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        con.layout().addItem(prx_btn)

    @staticmethod
    def get_category():
        return 'Core'

    def compute(self):
        self.out.call()

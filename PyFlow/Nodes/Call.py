from Qt import QtCore
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QGraphicsProxyWidget
from AbstractGraph import *
from Settings import *
from Node import Node


class Call(Node, NodeBase):
    def __init__(self, name, graph):
        super(Call, self).__init__(name, graph)
        self.out = self.addOutputPin("OUT", DataTypes.Exec, self.compute)

        self.process = False
        self.interval = 0.0
        self.counter = 0.0

        self.spin_box = QDoubleSpinBox()
        self.spin_box.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.spin_box.setMinimum(0.01)
        self.spin_box.setMaximum(60.0)
        self.spin_box.setValue(0.2)

        self.cb = QCheckBox()
        self.cb.stateChanged.connect(lambda: self.start(self.spin_box.value()))
        prx_cb = QGraphicsProxyWidget()
        prx_cb.setWidget(self.cb)

        prx_sb = QGraphicsProxyWidget()
        prx_sb.setWidget(self.spin_box)

        pb = QPushButton('call')
        pb.setMaximumWidth(30)
        con = self.add_container(PinTypes.Input)
        con2 = self.add_container(PinTypes.Input)

        pb.clicked.connect(self.compute)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        con.layout().addItem(prx_sb)
        con2.layout().addItem(prx_cb)
        con2.layout().addItem(prx_btn)

    def stop(self):
        self.process = False
        self.counter = 0.0

    def start(self, deltatime):
        if self.cb.isChecked():
            self.interval = deltatime
            self.process = True
        else:
            self.stop()

    def Tick(self, delta):
        if self.process:
            if self.counter + delta < self.interval:
                self.counter += delta
            else:
                self.compute()
                self.counter = 0.0

    @staticmethod
    def category():
        return 'Utils'

    def compute(self):
        self.out.call()

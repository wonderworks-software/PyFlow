from Qt import QtCore
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from AbstractGraph import *
from Settings import *
from Node import Node


class RequestNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(RequestNode, self).__init__(name, graph)
        self.input = self.addInputPin('input', DataTypes.Any)
        self.input.pinDisconnected = self.input_disconnected
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cb = QCheckBox()
        pb = QPushButton('get')
        pb.setMaximumWidth(25)
        self.process = False

        con = self.addContainer(PinTypes.Output)
        con2 = self.addContainer(PinTypes.Output)

        self.spin_box.setMinimum(0.01)
        self.spin_box.setMaximum(60.0)
        self.spin_box.setValue(0.2)
        prx_sb_delta_time = QGraphicsProxyWidget()
        prx_sb_delta_time.setWidget(self.spin_box)

        pb.clicked.connect(self.compute)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        self.interval = 0.0
        self.counter = 0.0
        self.cb.stateChanged.connect(lambda: self.start(self.spin_box.value()))
        prx_cb = QGraphicsProxyWidget()
        prx_cb.setWidget(self.cb)

        con2.layout().addItem(prx_cb)
        con2.layout().addItem(prx_btn)
        con.layout().addItem(prx_sb_delta_time)

    def input_disconnected(self, other):
        if not self.input.hasConnections():
            self.input._connected = False
            self.stop()
            self.cb.setCheckState(QtCore.Qt.Unchecked)

    @staticmethod
    def category():
        return 'Utils'

    def Tick(self, delta):
        if self.process and self.input._connected:
            if self.counter + delta < self.interval:
                self.counter += delta
            else:
                self.compute()
                self.counter = 0.0

    def stop(self):
        self.process = False
        self.counter = 0.0

    def start(self, deltatime):
        if self.cb.isChecked():
            self.interval = deltatime
            self.process = True
        else:
            self.stop()

    def compute(self):
        # check if any dirty nodes before connected Pin.
        # randint for example
        # if so push forward and recompute

        behind_dirty_ports = [p for p in find_ports_behind(self.input) if p.dirty is True]
        shouldRecalc = (not len(behind_dirty_ports) == 0)
        if shouldRecalc:
            # push from dirty ports
            # request data
            for p in behind_dirty_ports:
                push(p)

        data = self.input.getData()
        self.graph().writeToConsole(str(data))
        print(str(data))

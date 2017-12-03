from Qt import QtCore
from Qt.QtWidgets import QSpinBox
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from AbstractGraph import *
from Settings import *
from Node import Node


class RequestNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(RequestNode, self).__init__(name, graph)
        self.input = self.add_input_port('input', DataTypes.Any)
        self.looper = QtCore.QTimer()
        self.spin_box = QSpinBox()
        self.cb = QCheckBox()
        pb = QPushButton('request')
        self.looper.timeout.connect(self.compute)

        con = self.add_container(PinTypes.Output)
        con2 = self.add_container(PinTypes.Output)

        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(5000)
        self.spin_box.setValue(100)
        prx_sb_delta_time = QGraphicsProxyWidget()
        prx_sb_delta_time.setWidget(self.spin_box)

        pb.clicked.connect(self.compute)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)

        self.cb.stateChanged.connect(lambda: self.startEval(self.spin_box.value()))
        prx_cb = QGraphicsProxyWidget()
        prx_cb.setWidget(self.cb)

        con2.layout().addItem(prx_cb)
        con2.layout().addItem(prx_btn)
        con.layout().addItem(prx_sb_delta_time)

    @staticmethod
    def get_category():
        return 'Core'

    def startEval(self, deltatime):
        if self.cb.isChecked():
            self.looper.start(deltatime)
        else:
            self.looper.stop()

    def kill(self):
        Node.kill(self)
        if self.looper.isActive():
            self.looper.stop()

    def compute(self):
        # check if any dirty nodes before connected port.
        # randint for example
        # if so push forward and recompute

        behind_dirty_ports = [p for p in find_ports_behind(self.input) if p.dirty is True]
        shouldRecalc = (not len(behind_dirty_ports) == 0)
        if shouldRecalc:
            # push from dirty ports
            # request data
            for p in behind_dirty_ports:
                push(p)

        data = self.input.get_data()
        self.graph().write_to_console(str(data), True)

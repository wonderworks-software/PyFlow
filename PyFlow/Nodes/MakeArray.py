from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget


class MakeArray(Node, NodeBase):
    def __init__(self, name, graph, ports_number=0, w=60):
        super(MakeArray, self).__init__(name, graph, w, spacings=Spacings)
        self.ports_number = ports_number

        con = self.add_container(PinTypes.Output)

        pb = QPushButton('+')
        pb.setMaximumWidth(30)
        pb.clicked.connect(self.addInPort)
        prx_btn = QGraphicsProxyWidget()
        prx_btn.setWidget(pb)
        con.layout().addItem(prx_btn)

        self.height_step = pb.size().height()

        self.out_arr = self.add_output_port('out', DataTypes.Array)

    def post_create(self):
        for i in range(self.ports_number):
            self.addInPort()
        self.label().setPos(0, -self.label().boundingRect().height())
        super(MakeArray, self).post_create()

    def save_command(self):
        return "createNode ~type {0} ~count {4} ~x {1} ~y {2} ~n {3}\n".format(self.__class__.__name__, self.scenePos().x(), self.scenePos().y(), self.name, len(self.inputs))

    def addInPort(self):
        index = len(self.inputs)
        port = self.add_input_port(str(index), DataTypes.Any)
        portAffects(port, self.out_arr)
        push(self.out_arr)
        self.update_ports()

    @staticmethod
    def category():
        return 'Array'

    def compute(self):
        self.out_arr.set_data(list([i.get_data() for i in self.inputs]))

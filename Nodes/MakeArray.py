from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class MakeArray(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(MakeArray, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        self.id = 0
        AGNode.__init__(self, name, graph)
        lyt = self.add_layout()

        pb = QtGui.QPushButton('+')
        pb.clicked.connect(self.addInPort)
        prx_btn = QtGui.QGraphicsProxyWidget()
        prx_btn.setWidget(pb)
        lyt.addItem(prx_btn)

        self.height_step = pb.size().height()

        self.out_arr = self.add_output_port('out', AGPortDataTypes.tArray)

    def addInPort(self):
        port = self.add_input_port(str(self.id), AGPortDataTypes.tAny)
        self.h += self.height_step
        portAffects(port, self.out_arr)
        self.id += 1

    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):
        self.out_arr.set_data(list([i.get_data() for i in self.inputs]), False)


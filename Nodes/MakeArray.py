from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class MakeArray(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(MakeArray, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.out_arr = self.add_output_port('out', AGPortDataTypes.tArray)

    def compute(self):

        self.out_arr.set_data(list(), False)

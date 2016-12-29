from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ToString(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ToString, self).__init__(name, graph,
                                      w=150, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_data = self.add_input_port('in', AGPortDataTypes.tAny)
        self.out_data = self.add_output_port('out', AGPortDataTypes.tString)
        portAffects(self.in_data, self.out_data)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):

        out_data = self.in_data.get_data()
        try:
            self.out_data.set_data(str(out_data), False)
        except Exception, e:
            print e

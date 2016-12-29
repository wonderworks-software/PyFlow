from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ToInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ToInt, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp = self.add_input_port('float', AGPortDataTypes.tNumeric)
        self.out = self.add_output_port('int', AGPortDataTypes.tNumeric)
        portAffects(self.inp, self.out)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):

        data = self.inp.get_data()
        try:
            self.out.set_data(int(data), False)
        except Exception, e:
            self.graph.write_to_console("[ERROR] {0}".format(e))

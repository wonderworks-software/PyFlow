from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class StringToInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(StringToInt, self).__init__(name, graph,
                                      w=150, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_str = self.add_input_port('str', AGPortDataTypes.tString)
        self.out_int = self.add_output_port('int', AGPortDataTypes.tNumeric)
        portAffects(self.in_str, self.out_int)

    def compute(self):

        str_data = self.in_str.get_data()
        try:
            self.out_int.set_data(int(str_data), False)
        except Exception, e:
            print e

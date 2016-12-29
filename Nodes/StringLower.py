from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class StringLower(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(StringLower, self).__init__(name, graph,
                                      w=150, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_str = self.add_input_port('str', AGPortDataTypes.tString)
        self.out_str = self.add_output_port('lower str', AGPortDataTypes.tString)
        portAffects(self.in_str, self.out_str)

    @staticmethod
    def get_category():
        return 'StringUtils'

    def compute(self):

        str_data = self.in_str.get_data()
        try:
            self.out_str.set_data(str_data.lower(), False)
        except Exception, e:
            print e

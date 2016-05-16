from AGraphPySide import BaseNode
from AbstractGraph import *


class StringAppend(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(StringAppend, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.first = self.add_input_port('first', AGPortDataTypes.tString)
        self.second = self.add_input_port('second', AGPortDataTypes.tString)
        self.output = self.add_output_port('output', AGPortDataTypes.tString)
        portAffects(self.first, self.output)
        portAffects(self.second, self.output)

    def compute(self):

        first_str = self.first.get_data()
        second_str = self.second.get_data()
        try:
            result = first_str + second_str
            self.output.set_data(result, True)
        except Exception, e:
            print e

from AGraphPySide import BaseNode
from AbstractGraph import *


class StringReplace(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        BaseNode.Node.__init__(self, name, graph)
        self.first = self.add_input_port('source', AGPortDataTypes.tString)
        self.old_ptn = self.add_input_port('old pattern', AGPortDataTypes.tString)
        self.new_ptn = self.add_input_port('new pattern', AGPortDataTypes.tString)
        self.output = self.add_output_port('output', AGPortDataTypes.tString)
        portAffects(self.first, self.output)
        portAffects(self.old_ptn, self.output)
        portAffects(self.new_ptn, self.output)

    @staticmethod
    def get_category():
        return 'StringUtils'

    def compute(self):

        first_str = self.first.get_data()
        old_ptn = self.old_ptn.get_data()
        new_ptn = self.new_ptn.get_data()
        try:
            result = first_str.replace(old_ptn, new_ptn)
            self.output.set_data(result, False)
        except Exception, e:
            print e

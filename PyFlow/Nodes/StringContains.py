from Node import Node
from AbstractGraph import *


class StringContains(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringContains, self).__init__(name, graph)
        self.first = self.add_input_port('source', DataTypes.String)
        self.second = self.add_input_port('pattern', DataTypes.String)
        self.output = self.add_output_port('out', DataTypes.Bool)
        portAffects(self.first, self.output)
        portAffects(self.second, self.output)

    @staticmethod
    def get_category():
        return 'String'

    def compute(self):

        first_str = self.first.get_data()
        second_str = self.second.get_data()
        try:
            result = second_str in first_str
            self.output.set_data(result)
        except Exception, e:
            print e

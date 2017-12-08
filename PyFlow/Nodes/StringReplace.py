from Node import Node
from Settings import *
from AbstractGraph import *


class StringReplace(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringReplace, self).__init__(name, graph, spacings=Spacings)
        self.first = self.add_input_port('source', DataTypes.String)
        self.old_ptn = self.add_input_port('old pattern', DataTypes.String)
        self.new_ptn = self.add_input_port('new pattern', DataTypes.String)
        self.output = self.add_output_port('output', DataTypes.String)
        portAffects(self.first, self.output)
        portAffects(self.old_ptn, self.output)
        portAffects(self.new_ptn, self.output)

    @staticmethod
    def get_category():
        return 'String'

    def compute(self):

        first_str = self.first.get_data()
        old_ptn = self.old_ptn.get_data()
        new_ptn = self.new_ptn.get_data()
        try:
            result = first_str.replace(old_ptn, new_ptn)
            self.output.set_data(result)
        except Exception, e:
            print e

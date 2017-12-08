from AbstractGraph import *
from Settings import *
from Node import Node


class StringCapitalize(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringCapitalize, self).__init__(name, graph, spacings=Spacings)
        self.in_str = self.add_input_port('str', DataTypes.String)
        self.out_str = self.add_output_port('capitalized str', DataTypes.String)
        portAffects(self.in_str, self.out_str)

    @staticmethod
    def get_category():
        return 'String'

    def compute(self):

        str_data = self.in_str.get_data()
        try:
            self.out_str.set_data(str_data.capitalize())
        except Exception, e:
            print e

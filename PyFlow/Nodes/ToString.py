from AbstractGraph import *
from Settings import *
from Node import Node


class ToString(Node, NodeBase):
    def __init__(self, name, graph):
        super(ToString, self).__init__(name, graph, spacings=Spacings)
        self.in_data = self.add_input_port('in', DataTypes.Any)
        self.out_data = self.add_output_port('out', DataTypes.String)
        portAffects(self.in_data, self.out_data)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):

        out_data = self.in_data.get_data()
        try:
            self.out_data.set_data(str(out_data))
        except Exception, e:
            print e

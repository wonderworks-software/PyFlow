from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node


class StringToFloat(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringToFloat, self).__init__(name, graph, spacings=Spacings)
        self.in_str = self.add_input_port('str', DataTypes.String)
        self.out_flt = self.add_output_port('float', DataTypes.Float)
        portAffects(self.in_str, self.out_flt)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):

        str_data = self.in_str.get_data()
        try:
            self.out_flt.set_data(float(str_data), False)
        except Exception, e:
            print e

from AbstractGraph import *
from Settings import *
from Node import Node


class Len(Node, NodeBase):
    def __init__(self, name, graph):
        super(Len, self).__init__(name, graph, spacings=Spacings)
        self.in_arr = self.add_input_port('iterable', DataTypes.Any)
        self.out_len = self.add_output_port('len', DataTypes.Float)
        self.out_result = self.add_output_port('result', DataTypes.Bool)
        portAffects(self.in_arr, self.out_result)
        portAffects(self.in_arr, self.out_len)

    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):

        in_arr = self.in_arr.get_data()
        try:
            self.out_len.set_data(len(in_arr), False)
            self.out_result.set_data(True, False)
        except Exception, e:
            self.out_result.set_data(False, False)
            print e

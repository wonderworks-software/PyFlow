from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node


class FloatToInt(Node, NodeBase):
    def __init__(self, name, graph):
        super(FloatToInt, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.add_input_port('float', DataTypes.Float)
        self.out = self.add_output_port('int', DataTypes.Float)
        portAffects(self.inp, self.out)

    @staticmethod
    def get_category():
        return 'Convert'

    @staticmethod
    def description():
        return "Converts float to integer"

    def compute(self):

        data = self.inp.get_data()
        try:
            self.out.set_data(int(data), False)
        except Exception, e:
            self.graph.write_to_console("[ERROR] {0}".format(e))

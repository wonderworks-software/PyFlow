from AbstractGraph import *
from Settings import *
from Node import Node


class IsArray(Node, NodeBase):
    def __init__(self, name, graph):
        super(IsArray, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.add_input_port('obj', DataTypes.Any)
        self.out = self.add_output_port('out', DataTypes.Bool)
        portAffects(self.inp, self.out)

    @staticmethod
    def category():
        return 'Conditions'

    def compute(self):

        data = self.inp.get_data()
        result = False
        try:
            len(data)
            result = True
        except Exception, e:
            result = False
            self.graph.write_to_console("[ERROR] {0}. {1}".format(self.__class__.__name__, e))
        self.out.set_data(result)

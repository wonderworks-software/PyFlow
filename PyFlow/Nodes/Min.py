from AbstractGraph import *
from Settings import *
from Node import Node

DESC = '''returns minimum element
of iterable object.
'''


class Min(Node, NodeBase):
    def __init__(self, name, graph):
        super(Min, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.add_input_port('in', DataTypes.Any)
        self.out = self.add_output_port('min', DataTypes.Any)
        portAffects(self.inp, self.out)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        inp = self.inp.get_data()
        try:
            self.out.set_data(min(inp))
        except Exception as e:
            print(e)

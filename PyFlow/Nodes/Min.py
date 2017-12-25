from AbstractGraph import *
from Settings import *
from Node import Node

DESC = '''returns minimum element
of iterable object.
'''


class Min(Node, NodeBase):
    def __init__(self, name, graph):
        super(Min, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.addInputPin('in', DataTypes.Any)
        self.out = self.addOutputPin('min', DataTypes.Any)
        portAffects(self.inp, self.out)

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        inp = self.inp.getData()
        try:
            self.out.setData(min(inp))
        except Exception as e:
            print(e)

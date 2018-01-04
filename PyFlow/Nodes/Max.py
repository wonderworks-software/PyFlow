from AbstractGraph import *
from Settings import *
from Node import Node

DESC = '''returns maximum element of iterable object
'''


class Max(Node, NodeBase):
    def __init__(self, name, graph):
        super(Max, self).__init__(name, graph, spacings=Spacings)
        self.inp0 = self.addInputPin('in', DataTypes.Any)
        self.out0 = self.addOutputPin('out', DataTypes.Any)
        pinAffects(self.inp0, self.out0)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.Any]}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.getData()
        try:
            self.out0.setData(max(data))
        except Exception as e:
            print(e)

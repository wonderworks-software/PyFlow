from AbstractGraph import *
from Settings import *
from Node import Node


class Not(Node, NodeBase):
    def __init__(self, name, graph):
        super(Not, self).__init__(name, graph, spacings=Spacings)
        self.in_bool = self.addInputPin('in', DataTypes.Bool)
        self.out_bool = self.addOutputPin('out', DataTypes.Bool)
        portAffects(self.in_bool, self.out_bool)

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.Bool]

    @staticmethod
    def description():
        return 'flips boolean'

    def compute(self):

        in_bool = self.in_bool.getData()
        try:
            self.out_bool.setData(not in_bool)
        except Exception as e:
            print(e)

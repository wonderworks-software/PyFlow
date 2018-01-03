from Node import Node
from AbstractGraph import *


class IsGreaterThan(Node, NodeBase):
    def __init__(self, name, graph):
        super(IsGreaterThan, self).__init__(name, graph)
        self.inputA = self.addInputPin('inputA', DataTypes.Float)
        self.inputB = self.addInputPin('inputB', DataTypes.Float)
        self.output = self.addOutputPin('output', DataTypes.Bool)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.Float]

    @staticmethod
    def category():
        return 'Conditions'

    def compute(self):

        inp_a_data = self.inputA.getData()
        inp_b_data = self.inputB.getData()
        try:
            if inp_a_data > inp_b_data:
                self.output.setData(True)
            else:
                self.output.setData(False)
        except Exception, e:
            print e
            self.output.setData(False)

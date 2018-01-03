from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class IntToFloat(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(IntToFloat, self).__init__(name, graph)
        self.inp0 = self.addInputPin('int', DataTypes.Int, hideLabel=True, bCreateInputWidget=False)
        self.out0 = self.addOutputPin('float', DataTypes.Float, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Int], 'outputs': [DataTypes.Float]}

    @staticmethod
    def category():
        return 'Convert'

    @staticmethod
    def description():
        return "Converts integer to float"

    @staticmethod
    def keywords():
        return []

    def compute(self):
        self.out0.setData(float(self.inp0.getData()))

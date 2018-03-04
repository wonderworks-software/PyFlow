from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


class enumNode(Node):
    def __init__(self, name, graph):
        super(enumNode, self).__init__(name, graph)
        self.inp0 = self.addInputPin('in0', DataTypes.Enum, userStructClass=Direction, defaultValue=Direction.Left)
        self.out0 = self.addOutputPin('out0', DataTypes.Bool, defaultValue=True)
        pinAffects(self.inp0, self.out0)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Enum], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'default description'

    def compute(self):
        en = self.inp0.getData()
        if en == Direction.Left:
            self.out0.setData(True)
        else:
            self.out0.setData(False)

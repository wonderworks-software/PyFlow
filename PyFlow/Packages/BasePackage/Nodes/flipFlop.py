from PyFlow.Core import NodeBase


class flipFlop(NodeBase):
    def __init__(self, name):
        super(flipFlop, self).__init__(name)
        self.bState = True
        self.inp0 = self.addInputPin('in0', DataTypes.Exec, self.compute)
        self.outA = self.addOutputPin('A', DataTypes.Exec)
        self.outB = self.addOutputPin('B', DataTypes.Exec)
        self.bIsA = self.addOutputPin('IsA', DataTypes.Bool)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec], 'outputs': [DataTypes.Exec, DataTypes.Bool]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Changes flow each time called'

    def compute(self):
        if self.bState:
            self.bIsA.setData(self.bState)
            self.outA.call()
        else:
            self.bIsA.setData(self.bState)
            self.outB.call()
        self.bState = not self.bState

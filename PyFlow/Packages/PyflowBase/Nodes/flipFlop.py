from PyFlow.Core import NodeBase


class flipFlop(NodeBase):
    def __init__(self, name, parent):
        super(flipFlop, self).__init__(name)
        self.bState = True
        self.inp0 = self.addInputPin('in0', 'ExecPin', None,  self.compute)
        self.outA = self.addOutputPin('A', 'ExecPin')
        self.outB = self.addOutputPin('B', 'ExecPin')
        self.bIsA = self.addOutputPin('IsA', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin'], 'outputs': ['ExecPin', 'BoolPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Changes flow each time called'

    def compute(self, *args, **kwargs):
        if self.bState:
            self.bIsA.setData(self.bState)
            self.outA.call(*args, **kwargs)
        else:
            self.bIsA.setData(self.bState)
            self.outB.call(*args, **kwargs)
        self.bState = not self.bState

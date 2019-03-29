from PyFlow.Core import NodeBase


class branch(NodeBase):
    def __init__(self, name):
        super(branch, self).__init__(name)
        self.trueExec = self.addOutputPin("True", 'ExecPin')
        self.falseExec = self.addOutputPin("False", 'ExecPin')
        self.inExec = self.addInputPin("In", 'ExecPin', defaultValue=None, foo=self.compute)
        self.condition = self.addInputPin("Condition", 'BoolPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'BoolPin'], 'outputs': ['BoolPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self, *args, **kwargs):
        data = self.condition.getData()
        if data:
            self.trueExec.call(*args, **kwargs)
        else:
            self.falseExec.call(*args, **kwargs)

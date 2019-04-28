from PyFlow.Core import NodeBase


class branch(NodeBase):
    def __init__(self, name):
        super(branch, self).__init__(name)
        self.trueExec = self.createOutputPin("True", 'ExecPin')
        self.falseExec = self.createOutputPin("False", 'ExecPin')
        self.inExec = self.createInputPin("In", 'ExecPin', defaultValue=None, foo=self.compute)
        self.condition = self.createInputPin("Condition", 'BoolPin')

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

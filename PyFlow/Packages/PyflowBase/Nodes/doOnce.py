from PyFlow.Core import NodeBase


class doOnce(NodeBase):
    def __init__(self, name):
        super(doOnce, self).__init__(name)
        self.inExec = self.createInputPin('inExec', 'ExecPin', self.compute)
        self.reset = self.createInputPin('Reset', 'ExecPin', self.OnReset)
        self.bStartClosed = self.createInputPin('Start closed', 'BoolPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.bClosed = False

    def OnReset(self):
        self.bClosed = False
        self.bStartClosed.setData(False)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'BoolPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Will fire off an execution pin just once. But can reset.'

    def compute(self, *args, **kwargs):
        bStartClosed = self.bStartClosed.getData()

        if not self.bClosed and not bStartClosed:
            self.completed.call(*args, **kwargs)
            self.bClosed = True
            self.bStartClosed.setData(False)

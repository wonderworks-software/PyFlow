from PyFlow.Core import NodeBase


class tick(NodeBase):
    def __init__(self, name):
        super(tick, self).__init__(name)
        self.enabled = self.createInputPin("enabled", 'BoolPin')
        self.out = self.createOutputPin("out", 'ExecPin')
        self.delta = self.createOutputPin("delta", 'FloatPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    def Tick(self, delta):
        super(tick, self).Tick(delta)
        bEnabled = self.enabled.getData()
        if bEnabled:
            self.delta.setData(delta)
            self.out.call()

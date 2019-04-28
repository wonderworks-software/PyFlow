from PyFlow.Core import NodeBase


class delay(NodeBase):
    def __init__(self, name):
        super(delay, self).__init__(name)
        self.inp0 = self.createInputPin('in0', 'ExecPin', None, self.compute)
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.2)
        self.out0 = self.createOutputPin('out0', 'ExecPin')
        self.process = False
        self._total = 0.0
        self._currentDelay = 0.0

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'FloatPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Delayed call'

    def callAndReset(self):
        self.out0.call()
        self.process = False
        self._total = 0.0

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def compute(self, *args, **kwargs):
        self._currentDelay = self.delay.getData()
        if not self.process:
            self.process = True

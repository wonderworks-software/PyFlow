from PyFlow.Core import NodeBase


class retriggerableDelay(NodeBase):
    def __init__(self, name):
        super(retriggerableDelay, self).__init__(name)
        self.inp0 = self.createInputPin('in0', 'ExecPin', None, self.compute)
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.5)
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
        return 'Delayed call. With ability to reset.'

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def callAndReset(self):
        self.out0.call()
        self.process = False
        self._total = 0.0

    def compute(self, *args, **kwargs):
        self._total = 0.0
        self.process = True
        self._currentDelay = self.delay.getData()

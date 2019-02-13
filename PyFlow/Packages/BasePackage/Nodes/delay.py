from PyFlow.Core import NodeBase

# TODO: remove QTimer since this is a dependency
from Qt.QtCore import QTimer


class delay(NodeBase):
    def __init__(self, name):
        super(delay, self).__init__(name)
        self.inp0 = self.addInputPin('in0', 'ExecPin', self.compute)
        self.delay = self.addInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.2)
        self.out0 = self.addOutputPin('out0', 'ExecPin')
        self.process = False

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

    def compute(self):
        if not self.process:
            self.process = True
            delay = self.delay.getData() * 1000.0
            QTimer.singleShot(delay, self.callAndReset)

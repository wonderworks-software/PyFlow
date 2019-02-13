from PyFlow.Core import NodeBase
# TODO: remove QTimer
from Qt.QtCore import QTimer


class retriggerableDelay(NodeBase):
    def __init__(self, name):
        super(retriggerableDelay, self).__init__(name)
        self.inp0 = self.addInputPin('in0', 'ExecPin', self.compute)
        self.delay = self.addInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.2)
        self.out0 = self.addOutputPin('out0', 'ExecPin')
        self.process = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.callAndReset)

    def kill(self):
        self.timer.stop()
        self.timer.timeout.disconnect()
        Node.kill(self)

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

    def callAndReset(self):
        self.out0.call()
        self.process = False
        self.timer.stop()

    def restart(self):
        delay = self.delay.getData() * 1000.0
        self.timer.stop()
        self.timer.start(delay)

    def compute(self):
        self.restart()

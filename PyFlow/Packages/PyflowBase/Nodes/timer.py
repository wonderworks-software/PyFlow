from Qt.QtCore import QTimer

from PyFlow.Core import NodeBase


## Timer node
class timer(NodeBase):
    def __init__(self, name):
        super(timer, self).__init__(name)
        self.out = self.createOutputPin("OUT", 'ExecPin')
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.resetPin = self.createInputPin("Reset", 'ExecPin', None, self.reset)
        self.interval = self.createInputPin("Delta(ms)", 'FloatPin')
        self.interval.setDefaultValue(0.2)
        self._timer = QTimer()
        self._timer.timeout.connect(self.compute)

    def kill(self):
        self._timer.stop()
        self._timer.timeout.disconnect()
        NodeBase.kill(self)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['FloatPin', 'ExecPin'], 'outputs': ['ExecPin']}

    def reset(self, *args, **kwargs):
        self.stop()
        self.start()

    def stop(self, *args, **kwargs):
        self._timer.stop()

    def start(self, *args, **kwargs):
        dt = self.interval.getData() * 1000.0
        self._timer.start(dt)

    @staticmethod
    def category():
        return 'Utils'

    def compute(self, *args, **kwargs):
        self.out.call(*args, **kwargs)

from PyFlow.Core import NodeBase


class deltaTime(NodeBase):
    def __init__(self, name):
        super(deltaTime, self).__init__(name)
        self._deltaTime = 0.0
        self._out0 = self.addOutputPin('out0', 'FloatPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': ['FloatPin']}

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Editor delta time.'

    def Tick(self, deltaTime):
        self._deltaTime = deltaTime

    def compute(self):
        self._out0.setData(self._deltaTime)

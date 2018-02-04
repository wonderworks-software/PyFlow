from Core.AbstractGraph import *
from Core.Settings import *
from Core import Node
from Qt.QtCore import QTimer


class delay(Node, NodeBase):
    def __init__(self, name, graph):
        super(delay, self).__init__(name, graph)
        self.inp0 = self.addInputPin('in0', DataTypes.Exec, self.compute)
        self.delay = self.addInputPin('delay(s)', DataTypes.Float)
        self.delay.setDefaultValue(0.2)
        self.out0 = self.addOutputPin('out0', DataTypes.Exec)
        self.process = False

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Float], 'outputs': [DataTypes.Exec]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return '''Delayed call.'''

    def callAndReset(self):
        self.out0.call()
        self.process = False

    def compute(self):
        if not self.process:
            self.process = True
            delay = self.delay.getData() * 1000.0
            QTimer.singleShot(delay, self.callAndReset)

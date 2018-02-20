from Qt import QtCore
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QDoubleSpinBox
from Qt.QtWidgets import QCheckBox
from Qt.QtWidgets import QGraphicsProxyWidget
from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


## Timer node
class timer(Node, NodeBase):
    def __init__(self, name, graph):
        super(timer, self).__init__(name, graph)
        self.out = self.addOutputPin("OUT", DataTypes.Exec, self.compute)
        self.beginPin = self.addInputPin("Begin", DataTypes.Exec, self.start)
        self.stopPin = self.addInputPin("Stop", DataTypes.Exec, self.stop)
        self.resetPin = self.addInputPin("Reset", DataTypes.Exec, self.reset)
        self.interval = self.addInputPin("Delta(ms)", DataTypes.Float)
        self.interval.setDefaultValue(0.2)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.compute)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Float, DataTypes.Exec], 'outputs': [DataTypes.Exec]}

    def reset(self):
        self.stop()
        self.start()

    def stop(self):
        self._timer.stop()

    def start(self):
        dt = self.interval.getData() * 1000.0
        self._timer.start(dt)

    @staticmethod
    def category():
        return 'Utils'

    def compute(self):
        self.out.call()

from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QMenu
from Pins import _Pin


class makeQuatArray(Node):
    def __init__(self, name, graph):
        super(makeQuatArray, self).__init__(name, graph)
        self.out0 = self.addOutputPin('quats', DataTypes.Array)
        self.menu = QMenu()
        self.action = self.menu.addAction('add input')
        self.action.triggered.connect(self.addInPin)

    def addInPin(self):
        p = self.addInputPin(str(len(self.inputs)), DataTypes.Quaternion)
        pinAffects(p, self.out0)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Quaternion], 'outputs': [DataTypes.Array]}

    @staticmethod
    def category():
        return 'GenericTypes'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'array of quaternions'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore dinamically created inputs
        for inp in jsonTemplate['inputs']:
            p = _Pin.deserialize(self, inp)
            pinAffects(p, self.out0)

    def compute(self):
        self.out0.setData(list([i.getData() for i in self.inputs.values()]))

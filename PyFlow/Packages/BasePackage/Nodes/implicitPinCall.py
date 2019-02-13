import uuid

from PyFlow.Core import NodeBase

# TODO: Move menu to ui node class. This is raw class which should work from concole without dependencies. Ui node class should be chosen here through the interface
from Qt.QtWidgets import QMenu


class implicitPinCall(NodeBase):
    def __init__(self, name, graph):
        super(implicitPinCall, self).__init__(name, graph)
        self.inExec = self.addInputPin('inp', 'ExecPin', None, self.compute)
        self.uidInp = self.addInputPin('UUID', 'StringPin')
        self.outExec = self.addOutputPin('out', 'ExecPin')
        self.menu = QMenu()
        self.actionFindPin = self.menu.addAction('Find pin')
        self.actionFindPin.triggered.connect(self.OnFindPin)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['StringPin', 'ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Implicit execution pin call by provided <a href="https://ru.wikipedia.org/wiki/UUID"> uuid</a>.\nUse this when pins are far from each other.'

    def OnFindPin(self):
        uidStr = self.uidInp.getData()
        if len(uidStr) == 0:
            return
        try:
            uid = uuid.UUID(uidStr)
            pin = self.graph().pins[uid]
            self.graph().centerOn(pin)
            pin.highlight()
        except Exception as e:
            print(e)
            pass

    def compute(self):
        uidStr = self.uidInp.getData()
        if len(uidStr) == 0:
            return
        uid = uuid.UUID(uidStr)
        if uid in self.graph().pins:
            pin = self.graph().pins[uid]
            if not pin.hasConnections():
                pin.call()

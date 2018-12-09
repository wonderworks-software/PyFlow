from PyFlow.Core import NodeBase

# remove menu
from Qt.QtWidgets import QMenu


class implicitPinCall(NodeBase):
    def __init__(self, name):
        super(implicitPinCall, self).__init__(name)
        self.inExec = self.addInputPin('inp', DataTypes.Exec, self.compute)
        self.uidInp = self.addInputPin('UUID', DataTypes.String)
        self.outExec = self.addOutputPin('out', DataTypes.Exec)
        self.menu = QMenu()
        self.actionFindPin = self.menu.addAction('Find pin')
        self.actionFindPin.triggered.connect(self.OnFindPin)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String, DataTypes.Exec], 'outputs': [DataTypes.Exec]}

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

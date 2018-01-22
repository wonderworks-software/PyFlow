from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QMenu


class CallPinByUid(Node):
    def __init__(self, name, graph):
        super(CallPinByUid, self).__init__(name, graph)
        self.inExec = self.addInputPin('inp', DataTypes.Exec, self.compute)
        self.uidInp = self.addInputPin('uuid', DataTypes.String)
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
        return 'Implicit execution pin call'

    def OnFindPin(self):
        uidStr = self.uidInp.getData()
        try:
            uid = uuid.UUID(uidStr)
            self.graph().findPin(uid)
        except Exception as e:
            print(e)
            pass

    def compute(self):
        '''
            1) get data from inputs
            2) do stuff
            3) put data to outputs
            4) call output execs
        '''

        uidStr = self.uidInp.getData()
        uid = uuid.UUID(uidStr)
        if uid in self.graph().pins:
            pin = self.graph().pins[uid]
            if not pin.hasConnections():
                pin.call()

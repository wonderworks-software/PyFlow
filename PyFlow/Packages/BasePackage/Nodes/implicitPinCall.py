import uuid

from PyFlow.UI.IContextMenu import IContextMenu
from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase


class implicitPinCall(NodeBase, IContextMenu):
    def __init__(self, name):
        super(implicitPinCall, self).__init__(name)
        self.inExec = self.addInputPin('inp', 'ExecPin', None, self.compute)
        self.uidInp = self.addInputPin('UUID', 'StringPin')
        self.outExec = self.addOutputPin('out', 'ExecPin')

    def getActions(self):
        contextMenuData = {
            "Find pin": self.OnFindPin
        }
        return contextMenuData

    @staticmethod
    def packageName():
        return PACKAGE_NAME

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
            self.graph().findPin(uid)
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

import uuid

from PyFlow.Core import NodeBase


class implicitPinCall(NodeBase):
    def __init__(self, name):
        super(implicitPinCall, self).__init__(name)
        self.inExec = self.addInputPin('inp', 'ExecPin', None, self.compute)
        self.uidInp = self.addInputPin('UUID', 'StringPin')
        self.outExec = self.addOutputPin('out', 'ExecPin')

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

    def compute(self, *args, **kwargs):
        uidStr = self.uidInp.getData()
        if len(uidStr) == 0:
            return
        uid = uuid.UUID(uidStr)
        if uid in self.graph().pins:
            pin = self.graph().pins[uid]
            if not pin.hasConnections():
                pin.call(*args, **kwargs)

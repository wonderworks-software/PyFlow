from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


class doOnce(NodeBase):
    def __init__(self, name):
        super(doOnce, self).__init__(name)
        self.inExec = self.addInputPin('inExec', DataTypes.Exec, self.compute)
        self.reset = self.addInputPin('Reset', DataTypes.Exec, self.OnReset)
        self.bStartClosed = self.addInputPin('Start closed', DataTypes.Bool)
        self.completed = self.addOutputPin('Completed', DataTypes.Exec)
        self.bClosed = False

    def OnReset(self):
        self.bClosed = False
        self.bStartClosed.setData(False)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Bool], 'outputs': [DataTypes.Exec]}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Will fire off an execution pin just once. But can reset.'

    def compute(self):
        bStartClosed = self.bStartClosed.getData()

        if not self.bClosed and not bStartClosed:
            self.completed.call()
            self.bClosed = True
            self.bStartClosed.setData(False)

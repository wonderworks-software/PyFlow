from PyFlow.Core import NodeBase
from PyFlow.Core import PinBase
from PyFlow.Core.Common import *


class switchOnString(NodeBase):
    def __init__(self, name):
        super(switchOnString, self).__init__(name)
        self.inExecPin = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.inString = self.createInputPin('String', 'StringPin')
        self.defaultPin = self.createOutputPin('Default', 'ExecPin')

    def addOutPin(self):
        name = self.getUniqPinName("option")
        p = self.createOutputPin(name, 'ExecPin')
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        pinAffects(self.inExecPin, p)
        return p

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'StringPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Execute output depending on input string'

    def compute(self, *args, **kwargs):
        string = self.inString.getData()
        namePinOutputsMap = self.namePinOutputsMap
        if string in namePinOutputsMap:
            namePinOutputsMap[string].call(*args, **kwargs)
        else:
            self.defaultPin.call(*args, **kwargs)

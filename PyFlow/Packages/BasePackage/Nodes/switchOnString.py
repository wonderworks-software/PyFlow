from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class switchOnString(NodeBase):
    def __init__(self, name):
        super(switchOnString, self).__init__(name)
        self.inExecPin = self.addInputPin('inExec', 'ExecPin', None, self.compute)
        self.inString = self.addInputPin('String', 'StringPin')
        self.defaultPin = self.addOutputPin('Default', 'ExecPin')

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def addOutPin(self):
        name = self.getUniqPinName("option")
        p = self.addOutputPin(name, 'ExecPin')
        pinAffects(self.inExecPin, p)
        if p.uid not in self.graph().pins:
            self.graph().pins[p.uid] = p
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

    def compute(self):
        string = self.inString.getData()
        if string in self.namePinOutputsMap:
            self.namePinOutputsMap[string].call()
        else:
            self.defaultPin.call()

from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *


class switchOnString(NodeBase):
    def __init__(self, name):
        super(switchOnString, self).__init__(name)
        self.inExecPin = self.addInputPin('inExec', 'ExecPin', self.compute)
        self.defaultPin = None
        self.outString = None
        self.inString = self.addInputPin('String', 'StringPin')
        self._map = {}

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def renameOutPin(self, oldName, newName):
        if oldName in self._map:
            self._map[oldName].setName(newName)

    def OnDebug(self):
        print(self._map.keys())

    def addOutPin(self):
        name = self.getUniqPinName("option")
        p = self.addOutputPin(name, 'ExecPin')

        pinAffects(self.inExecPin, p)
        self._map[name] = p

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

    def postCreate(self, jsonTemplate):
        NodeBase.postCreate(self, jsonTemplate)

        # restore dynamically created  outputs
        if len(jsonTemplate['outputs']) == 0:
            self.defaultPin = self.addOutputPin('Default', 'ExecPin')
            self.outString = self.addOutputPin('stringOut', 'StringPin')
            self.addOutPin()
            self.addOutPin()
        else:
            for out in jsonTemplate['outputs']:
                PinBase.deserialize(self, out)

    def compute(self):
        string = self.inString.getData()
        self.outString.setData(string)
        if string in self._map:
            self._map[string].call()
        else:
            self.defaultPin.call()

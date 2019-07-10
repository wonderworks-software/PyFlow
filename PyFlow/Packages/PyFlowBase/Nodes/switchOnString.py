from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class switchOnString(NodeBase):
    def __init__(self, name):
        super(switchOnString, self).__init__(name)
        self.inExecPin = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inString = self.createInputPin('string', 'StringPin')
        self.defaultPin = self.createOutputPin('default', 'ExecPin')
        self.headerColor = FLOW_CONTROL_COLOR

    def addOutPin(self):
        name = self.getUniqPinName("option")
        p = self.createOutputPin(name, 'ExecPin')
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        pinAffects(self.inExecPin, p)
        return p

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

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

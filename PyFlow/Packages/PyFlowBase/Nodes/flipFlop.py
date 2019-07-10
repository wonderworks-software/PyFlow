from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class flipFlop(NodeBase):
    def __init__(self, name):
        super(flipFlop, self).__init__(name)
        self.bState = True
        self.inp0 = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.outA = self.createOutputPin('A', 'ExecPin')
        self.outB = self.createOutputPin('B', 'ExecPin')
        self.bIsA = self.createOutputPin('IsA', 'BoolPin')
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('BoolPin')
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
        return 'Changes flow each time called'

    def compute(self, *args, **kwargs):
        if self.bState:
            self.bIsA.setData(self.bState)
            self.outA.call(*args, **kwargs)
        else:
            self.bIsA.setData(self.bState)
            self.outB.call(*args, **kwargs)
        self.bState = not self.bState

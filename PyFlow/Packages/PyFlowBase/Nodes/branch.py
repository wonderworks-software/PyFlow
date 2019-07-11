from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class branch(NodeBase):
    def __init__(self, name):
        super(branch, self).__init__(name)
        self.trueExec = self.createOutputPin("True", 'ExecPin')
        self.falseExec = self.createOutputPin("False", 'ExecPin')
        self.inExec = self.createInputPin("In", 'ExecPin', defaultValue=None, foo=self.compute)
        self.condition = self.createInputPin("Condition", 'BoolPin')
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def description():
        return """**If else** block."""

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self, *args, **kwargs):
        data = self.condition.getData()
        if data:
            self.trueExec.call(*args, **kwargs)
        else:
            self.falseExec.call(*args, **kwargs)

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class tick(NodeBase):
    def __init__(self, name):
        super(tick, self).__init__(name)
        self.enabled = self.createInputPin("enabled", 'BoolPin')
        self.out = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.delta = self.createOutputPin("delta", 'FloatPin')
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('FloatPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    def Tick(self, delta):
        super(tick, self).Tick(delta)
        bEnabled = self.enabled.getData()
        if bEnabled:
            self.delta.setData(delta)
            self.out.call()

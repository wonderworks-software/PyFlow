from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class delay(NodeBase):
    def __init__(self, name):
        super(delay, self).__init__(name)
        self.inp0 = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.2)
        self.out0 = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.process = False
        self._total = 0.0
        self._currentDelay = 0.0
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('FloatPin')
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
        return 'Delayed call'

    def callAndReset(self):
        self.out0.call()
        self.process = False
        self._total = 0.0

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def compute(self, *args, **kwargs):
        self._currentDelay = self.delay.getData()
        if not self.process:
            self.process = True

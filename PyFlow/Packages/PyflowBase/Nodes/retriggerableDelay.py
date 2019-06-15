from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper


class retriggerableDelay(NodeBase):
    def __init__(self, name):
        super(retriggerableDelay, self).__init__(name)
        self.inp0 = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.5)
        self.out0 = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.process = False
        self._total = 0.0
        self._currentDelay = 0.0

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
        return 'Delayed call. With ability to reset.'

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def callAndReset(self):
        self.out0.call()
        self.process = False
        self._total = 0.0

    def compute(self, *args, **kwargs):
        self._total = 0.0
        self.process = True
        self._currentDelay = self.delay.getData()

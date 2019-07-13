from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class charge(NodeBase):
    def __init__(self, name):
        super(charge, self).__init__(name)
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.amount = self.createInputPin('Amount', 'FloatPin')
        self.amount.setDefaultValue(1.0)

        self.step = self.createInputPin('Step', 'FloatPin')
        self.step.setDefaultValue(0.1)

        self.completed = self.createOutputPin('completed', 'ExecPin')
        self._currentAmount = 0
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
        return 'Each time node called it accumulates the step value.' +\
               'When accumulated value reaches **amount** - **completed** pin called.' +\
               'Useful when you need to wait some time inside some tick function.'

    def compute(self, *args, **kwargs):
        step = abs(self.step.getData())
        if (self._currentAmount + step) < abs(self.amount.getData()):
            self._currentAmount += step
            return
        self.completed.call(*args, **kwargs)
        self._currentAmount = 0.0

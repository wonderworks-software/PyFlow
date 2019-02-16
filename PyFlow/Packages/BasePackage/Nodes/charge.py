from PyFlow.Core import NodeBase
from PyFlow.Core.AGraphCommon import *


## charge node
#
# Each time node called it accumulates the step value.
# When accumulated value reaches "amount" - completed pin called.
# Useful when you need to wait some time inside some tick function.
class charge(NodeBase):
    def __init__(self, name):
        super(charge, self).__init__(name)
        self.inExec = self.addInputPin('inExec', 'ExecPin', self.compute)
        self.amount = self.addInputPin('Amount', 'FloatPin')
        self.amount.setDefaultValue(1.0)

        self.step = self.addInputPin('Step', 'FloatPin')
        self.step.setDefaultValue(0.1)

        self.completed = self.addOutputPin('completed', 'ExecPin')
        self._currentAmount = 0

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['FloatPin', 'ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Each time node called it accumulates the step value. \
        When accumulated value reaches <b>"amount"</b> - completed pin called.\n\
        Useful when you need to wait some time inside some tick function.'

    def compute(self):
        step = abs(self.step.getData())
        if (self._currentAmount + step) < abs(self.amount.getData()):
            self._currentAmount += step
            return
        self.completed.call()
        self._currentAmount = 0.0

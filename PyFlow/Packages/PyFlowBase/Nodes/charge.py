## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.PyFlow.Core import NodeBase
from PyFlow.PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.PyFlow.Core.Common import *
from PyFlow.PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


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
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
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

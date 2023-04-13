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
from PyFlow.PyFlow.Core.Common import *
from PyFlow.PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


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
        return 'Delayed call'

    def callAndReset(self):
        self.process = False
        self._total = 0.0
        self.out0.call()

    def Tick(self, delta):
        if self.process:
            self._total += delta
            if self._total >= self._currentDelay:
                self.callAndReset()

    def compute(self, *args, **kwargs):
        self._currentDelay = self.delay.getData()
        if not self.process:
            self.process = True

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

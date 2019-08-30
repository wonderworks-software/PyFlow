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
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class doN(NodeBase):
    def __init__(self, name):
        super(doN, self).__init__(name)
        self.enter = self.createInputPin('Enter', 'ExecPin', None, self.compute)
        self._N = self.createInputPin('N', 'IntPin')
        self._N.setData(10)
        self.reset = self.createInputPin('Reset', 'ExecPin', None, self.OnReset)

        self.completed = self.createOutputPin('Exit', 'ExecPin')
        self.counter = self.createOutputPin('Counter', 'IntPin')
        self.bClosed = False
        self._numCalls = 0
        self.headerColor = FLOW_CONTROL_COLOR

    def OnReset(self):
        self.bClosed = False
        self._numCalls = 0

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('IntPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('IntPin')
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
        return 'The DoN node will fire off an execution pin N times. After the limit has been reached,\
        it will cease all outgoing execution until a pulse is sent into its Reset input.'

    def compute(self, *args, **kwargs):
        maxCalls = self._N.getData()
        if not self.bClosed and self._numCalls <= maxCalls:
            self._numCalls += 1
            self.counter.setData(self._numCalls)
            self.completed.call(*args, **kwargs)

            # if next time we will reach the limit - close
            if (self._numCalls + 1) > maxCalls:
                self.bClosed = True

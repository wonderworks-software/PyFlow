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


class doOnce(NodeBase):
    def __init__(self, name):
        super(doOnce, self).__init__(name)
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.reset = self.createInputPin('Reset', 'ExecPin', None, self.OnReset)
        self.bStartClosed = self.createInputPin('Start closed', 'BoolPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.bClosed = False
        self.headerColor = FLOW_CONTROL_COLOR

    def OnReset(self):
        self.bClosed = False
        self.bStartClosed.setData(False)

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

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Will fire off an execution pin just once. But can reset.'

    def compute(self, *args, **kwargs):
        bStartClosed = self.bStartClosed.getData()

        if not self.bClosed and not bStartClosed:
            self.completed.call(*args, **kwargs)
            self.bClosed = True
            self.bStartClosed.setData(False)

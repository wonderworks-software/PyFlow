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
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
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

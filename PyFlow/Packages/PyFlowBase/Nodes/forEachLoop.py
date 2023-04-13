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


class forEachLoop(NodeBase):
    def __init__(self, name):
        super(forEachLoop, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.array = self.createInputPin('array', 'AnyPin', structure=StructureType.Array, constraint="1")
        self.array.enableOptions(PinOptions.AllowAny)

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.elem = self.createOutputPin('element', 'AnyPin', constraint="1")
        self.elem.enableOptions(PinOptions.AllowAny)
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Single)
        helper.addInputStruct(StructureType.Array)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter', 'for', 'loop', 'each']

    @staticmethod
    def description():
        return 'For each loop'

    def compute(self, *args, **kwargs):
        ls = self.array.getData()
        if len(ls) == 0:
            self.completed.call(*args, **kwargs)
        else:
            for i in ls:
                self.elem.setData(i)
                push(self.elem)
                self.loopBody.call(*args, **kwargs)
            self.completed.call(*args, **kwargs)

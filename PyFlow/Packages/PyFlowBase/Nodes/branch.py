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


class branch(NodeBase):
    def __init__(self, name):
        super(branch, self).__init__(name)
        self.trueExec = self.createOutputPin("True", "ExecPin")
        self.falseExec = self.createOutputPin("False", "ExecPin")
        self.inExec = self.createInputPin(
            "In", "ExecPin", defaultValue=None, callback=self.compute
        )
        self.condition = self.createInputPin("Condition", "BoolPin")
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def description():
        return """**If else** block."""

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("BoolPin")
        helper.addOutputDataType("ExecPin")
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "FlowControl"

    def compute(self, *args, **kwargs):
        data = self.condition.getData()
        if data:
            self.trueExec.call(*args, **kwargs)
        else:
            self.falseExec.call(*args, **kwargs)

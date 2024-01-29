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


from PyFlow.Core.Common import *
from PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core import NodeBase
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_ORANGE


class loopEnd(NodeBase):
    def __init__(self, name):
        super(loopEnd, self).__init__(name)
        self.inExec = self.createInputPin(
            DEFAULT_IN_EXEC_NAME, "ExecPin", None, self.compute
        )
        self.loopBeginNode = self.createInputPin("Paired block", "StringPin")
        self.loopBeginNode.setInputWidgetVariant("ObjectPathWidget")
        self.completed = self.createOutputPin("Completed", "ExecPin")
        self.headerColor = FLOW_CONTROL_ORANGE
        self.setExperimental()

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("ExecPin")
        helper.addInputDataType("StringPin")
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "FlowControl"

    @staticmethod
    def keywords():
        return ["iter", "end"]

    @staticmethod
    def description():
        return "For loop end block"

    def compute(self, *args, **kwargs):
        node = PathsRegistry().getEntity(self.loopBeginNode.getData())
        if node is not None:
            if node.graph() == self.graph():
                if node.loopEndNode.getData() != self.path():
                    self.setError("Invalid pair")
                    return
                if node.__class__.__name__ == "forLoopBegin":
                    node.prevIndex = node.currentIndex
                    node.currentIndex += 1
                    if node.currentIndex >= node.lastIndex.getData():
                        self.completed.call()
                else:
                    node.onNext()
            else:
                err = "block ends in different graphs"
                node.setError(err)
                self.setError(err)
        else:
            self.setError("Pair {} not found".format(self.loopBeginNode.getData()))

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
from PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_ORANGE


class whileLoopBegin(NodeBase):
    def __init__(self, name):
        super(whileLoopBegin, self).__init__(name)
        self.lastCondition = False
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.condition = self.createInputPin('Condition', 'BoolPin')
        self.loopEndNode = self.createInputPin('Paired block', 'StringPin')
        self.loopEndNode.setInputWidgetVariant("ObjectPathWIdget")

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.headerColor = FLOW_CONTROL_ORANGE
        self.setExperimental()

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'While loop begin block'

    def onNext(self, *args, **kwargs):
        currentCondition = self.condition.getData()
        if currentCondition:
            self.loopBody.call(*args, **kwargs)
        if self.lastCondition is True and currentCondition is False:
            endNodePath = self.loopEndNode.getData()
            loopEndNode = PathsRegistry().getEntity(endNodePath)
            loopEndNode.completed.call()
            self.lastCondition = False
            return
        self.lastCondition = currentCondition

    def compute(self, *args, **kwargs):
        endNodePath = self.loopEndNode.getData()
        loopEndNode = PathsRegistry().getEntity(endNodePath)
        if loopEndNode is not None:
            if loopEndNode.loopBeginNode.getData() != self.path():
                self.setError("Invalid pair")
                return
            if self.graph() is not loopEndNode.graph():
                err = "block ends in different graphs"
                self.setError(err)
                loopEndNode.setError(err)
                return
        else:
            self.setError("Pair {} not found".format(endNodePath))
            return

        self.onNext(*args, **kwargs)

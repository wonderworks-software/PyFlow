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


class whileLoop(NodeBase):
    def __init__(self, name):
        super(whileLoop, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.begin)
        self.bCondition = self.createInputPin('Condition', 'BoolPin')
        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.bProcess = False
        self._dirty = False
        self.headerColor = FLOW_CONTROL_COLOR

    def begin(self, *args, **kwargs):
        self.bProcess = True

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
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
        return []

    def Tick(self, deltaTime):
        currentCondition = self.bCondition.getData()

        if self.bProcess and currentCondition:
            self.loopBody.call()
            # when started mark dirty to call completed later
            if not self._dirty:
                self._dirty = True
            return
        else:
            self.bProcess = False

        # of _dirty is True that means condition been changed from True to False
        # so in that case call completed and set clean
        if self._dirty:
            self.completed.call()
            self._dirty = False

    @staticmethod
    def description():
        return 'The WhileLoop node will output a result so long as a specific condition is true. During each iteration of the loop, it checks to see the current status of its input boolean value. As soon as it reads false, the loop breaks.\nAs with While loops in programming languages, extra care must be taken to prevent infinite loops from occurring.'

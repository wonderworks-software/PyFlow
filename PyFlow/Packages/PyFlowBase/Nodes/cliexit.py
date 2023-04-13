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
from PyFlow.PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class cliexit(NodeBase):
    def __init__(self, name):
        super(cliexit, self).__init__(name)
        self.inp0 = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'CLI'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Stops cli program loop'

    def compute(self, *args, **kwargs):
        man = GraphManagerSingleton().get()
        man.terminationRequested = True

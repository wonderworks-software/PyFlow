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


class rerouteExecs(NodeBase):
    def __init__(self, name):
        super(rerouteExecs, self).__init__(name)
        self.input = self.createInputPin("in", 'ExecPin')
        self.output = self.createOutputPin("out", 'ExecPin')
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    def postCreate(self, jsonTemplate=None):
        super(rerouteExecs, self).postCreate(jsonTemplate=jsonTemplate)
        self.setName("reroute")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Common'

    def compute(self, *args, **kwargs):
        pass

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


class reroute(NodeBase):
    def __init__(self, name):
        super(reroute, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', structure=StructureType.Multi, constraint="1", structConstraint="1")
        self.output = self.createOutputPin("out", 'AnyPin', structure=StructureType.Multi, constraint="1", structConstraint="1")
        self.input.checkForErrors = False
        self.output.checkForErrors = False
        self.input.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.output.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'Common'

    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())

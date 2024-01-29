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


class address(NodeBase):
    def __init__(self, name):
        super(address, self).__init__(name)
        self.obj = self.createInputPin("obj", "AnyPin", structure=StructureType.Multi)
        self.obj.enableOptions(PinOptions.AllowAny)
        self.addr = self.createOutputPin("out", "StringPin")

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType("AnyPin")
        helper.addOutputDataType("StringPin")
        helper.addInputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return "Utils"

    @staticmethod
    def keywords():
        return ["id"]

    @staticmethod
    def description():
        return "Returns address of an object in memory"

    def compute(self, *args, **kwargs):
        self.addr.setData(hex(id(self.obj.getData())))

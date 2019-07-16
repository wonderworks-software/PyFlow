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
import ast


class stringToArray(NodeBase):
    def __init__(self, name):
        super(stringToArray, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'StringPin', structure=PinStructure.Single)
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Array)
        self.result = self.createOutputPin('result', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('AnyPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Array)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'GenericTypes'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a list from ast.literal_eval(data) and then converts to output DataType'

    def compute(self, *args, **kwargs):
        outArray = []
        stringData = "[%s]"%self.arrayData.getData()
        if self.outArray.dataType == "AnyPin":
            self.outArray.setData(outArray)
            self.result.setData(False)
        else:
            splited = ast.literal_eval(stringData)
            self.outArray.setData(splited)
            self.result.setData(True)

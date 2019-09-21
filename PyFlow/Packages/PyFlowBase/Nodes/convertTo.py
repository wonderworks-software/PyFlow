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
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow import CreateRawPin
from copy import copy


class convertTo(NodeBase):
    def __init__(self, name):
        super(convertTo, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', defaultValue=None)
        self.output = self.createOutputPin("result", 'AnyPin', defaultValue=None)
        pinAffects(self.input, self.output)
        self.input.enableOptions(PinOptions.AllowAny)
        self.pinTypes = []
        for pinClass in getAllPinClasses():
            if pinClass.IsValuePin():
                self.pinTypes.append(pinClass.__name__)
        self.bCacheEnabled = False

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'GenericTypes'
        
    def serialize(self):      
        orig = super(convertTo, self).serialize()
        orig["currDataType"] = self.output.dataType
        return orig

    def postCreate(self, jsonTemplate=None):
        super(convertTo, self).postCreate(jsonTemplate)
        if "currDataType" in jsonTemplate:
            self.updateType(self.pinTypes.index(jsonTemplate["currDataType"]))

    def updateType(self, dataTypeIndex):
        self.output.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.changeType(self.pinTypes[dataTypeIndex], True)
        self.output.disableOptions(PinOptions.ChangeTypeOnConnection)

    def changeType(self, dataType, init=False):
        b = self.output.initType(dataType, init)

    def compute(self, *args, **kwargs):
        otherClass = findPinClassByType(self.output.dataType)
        self.output.setData(otherClass.processData(self.input.getData()))

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
from PyFlow.Core.structs import splineRamp

class colorRamp(NodeBase):
    def __init__(self, name):
        super(colorRamp, self).__init__(name)
        self.bCacheEnabled = False
        self.input = self.createInputPin('input', 'FloatPin', structure=PinStructure.Multi)
        self.input.enableOptions(PinOptions.AlwaysPushDirty)
        self.output = self.createOutputPin('result', 'FloatPin', structure=PinStructure.Array)
        self.output.enableOptions(PinOptions.AlwaysPushDirty)
        self.ramp = splineRamp()
        self._curveTypes = ["linear", "bezier"]
        self._curveType = 0

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('FloatPin')
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Array)
        return helper

    def serialize(self):
        orig = super(colorRamp, self).serialize()
        orig["ramp"] = [[x.getU(), x.getV()] for x in self.ramp.sortedItems()]
        orig["curveType"] = self._curveType
        return orig

    def postCreate(self, jsonTemplate=None):
        super(colorRamp, self).postCreate(jsonTemplate)
        if "ramp" in jsonTemplate:
            for x in jsonTemplate["ramp"]:
                self.ramp.addItem(x[0],x[1])
        if "curveType" in jsonTemplate:
                self._curveType = jsonTemplate["curveType"]

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return ["fcurve","ramp","curve"]

    @staticmethod
    def description():
        return 'Editable fCurve maped from 0 to 1, click on empty Space to add point, and right Click to delete point'

    def compute(self, *args, **kwargs):
        bezier = self._curveTypes[self._curveType] == "bezier"
        if not self.input.isArray():
            self.output.setData(self.ramp.evaluateAt(self.input.getData(),bezier))
        else:
            result = []
            for i in self.input.getData():
                result.append(self.ramp.evaluateAt(i,bezier))
            self.output.setData(result)
        push(self.output)

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
from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
import uuid

class switch(NodeBase):
    def __init__(self, name):
        super(switch, self).__init__(name)
        self.inExecPin = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.inVal = self.createInputPin('in', 'AnyPin', supportedPinDataTypes=['StringPin', 'IntPin', 'BoolPin'])
        self.defaultPin = self.createOutputPin('default', 'ExecPin')
        self.headerColor = FLOW_CONTROL_COLOR

    def postCreate(self, jsonTemplate=None):
        super(switch, self).postCreate(jsonTemplate=jsonTemplate)
        existingPins = self.namePinOutputsMap
        if jsonTemplate is not None:
            sortedOutputs = sorted(jsonTemplate['outputs'], key=lambda pinDict: pinDict["pinIndex"])
            for pinJson in sortedOutputs:
                if pinJson['name'] not in existingPins:
                    inDyn = self.addOutPin(pinJson['name'])
                    inDyn.uid = uuid.UUID(pinJson['uuid'])
                    
    def addOutPin(self, name):
        p = self.createOutputPin(name, 'ExecPin')
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic)
        pinAffects(self.inExecPin, p)
        return p

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('StringPin')
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

    @staticmethod
    def description():
        return 'Execute output depending on input string'

    def compute(self, *args, **kwargs):
        string = str(self.inVal.getData())
        namePinOutputsMap = self.namePinOutputsMap
        if string in namePinOutputsMap:
            namePinOutputsMap[string].call(*args, **kwargs)
        else:
            self.defaultPin.call(*args, **kwargs)

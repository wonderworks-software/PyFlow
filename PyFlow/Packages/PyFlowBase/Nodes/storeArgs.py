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


import asyncio
import time

from PyFlow.Core import NodeBase, PinBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
import json


class storeArgs(NodeBase):
    def __init__(self, name):
        super(storeArgs, self).__init__(name)
        self.bCacheEnabled = False
        self.hold_pos = self.createInputPin('0', 'StringPin', "")
        self.combine_result = self.createOutputPin('combine_result', 'StringPin', "")

    def addInPin(self, name, dataType):
        p_in = self.createInputPin(name, dataType)
        p_in.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic | PinOptions.Storable)
        return p_in
    
    def addOutPin(self, name, dataType):
        p_out = self.createOutputPin(name, dataType)
        return p_out

    def postCreate(self, jsonTemplate=None):
        super(storeArgs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for pinJson in sortedInputs:
                if pinJson['name'] not in existingPins:
                    pinDyn = self.addInPin(pinJson['name'], pinJson["dataType"])
                    pinDyn.uid = uuid.UUID(pinJson['uuid'])
                    try:
                        val = json.loads(pinJson['value'], cls=pinDyn.jsonDecoderClass())
                        pinDyn.setData(val)
                    except:
                        pinDyn.setData(pinDyn.defaultValue())
            sortedOutputs = sorted(jsonTemplate["outputs"], key=lambda x: x["pinIndex"])
            for pinJson in sortedOutputs:
                if pinJson['name'] not in existingPins:
                    pinDyn = self.addOutPin(pinJson['name'], pinJson["dataType"])
                    pinDyn.uid = uuid.UUID(pinJson['uuid'])
                    try:
                        val = json.loads(pinJson['value'], cls=pinDyn.jsonDecoderClass())
                        pinDyn.setData(val)
                    except:
                        pinDyn.setData(pinDyn.defaultValue())

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        return helper

    @staticmethod
    def category():
        return 'Cmd'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'store args'

    def compute(self, *args, **kwargs):
        cmd_line = ""
        output_map = self.namePinOutputsMap
        for elem in self.orderedInputs.values():
            name = elem.name.lstrip("> ")
            if name in output_map:
                output_map[name].setData(elem.getData())
            if 0 == len(name) or name.isdigit():
                cmd_line += " {0} ".format(elem.getData())
                continue
            if 1 == len(name) and name.isalpha():
                cmd_line += " -{0} {1} ".format(name ,elem.getData()) 
                continue
            if name[:1] == "-":
                cmd_line += " {0} {1} ".format(name ,elem.getData())    
                continue 
            cmd_line += " --{0} {1} ".format(name ,elem.getData()) 
        self.combine_result.setData(cmd_line)
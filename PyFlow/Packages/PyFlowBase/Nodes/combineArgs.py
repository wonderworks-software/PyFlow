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


class combineArgs(NodeBase):
    def __init__(self, name):
        super(combineArgs, self).__init__(name)
        self.bCacheEnabled = False
        self.combine_result = self.createOutputPin('combine_result', 'StringPin', "")

    def addInPin(self, name, dataType):
        p = self.createInputPin(name, dataType)
        p.enableOptions(PinOptions.RenamingEnabled | PinOptions.Dynamic 
                        | PinOptions.AllowMultipleConnections | PinOptions.Storable)
        return p

    def postCreate(self, jsonTemplate=None):
        super(combineArgs, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamically created pins
        existingPins = self.namePinInputsMap
        if jsonTemplate is not None:
            sortedInputs = sorted(jsonTemplate["inputs"], key=lambda x: x["pinIndex"])
            for inPinJson in sortedInputs:
                if inPinJson['name'] not in existingPins:
                    inDyn = self.addInPin(inPinJson['name'], inPinJson["dataType"])
                    inDyn.uid = uuid.UUID(inPinJson['uuid'])
                    try:
                        val = json.loads(inPinJson['value'], cls=inDyn.jsonDecoderClass())
                        inDyn.setData(val)
                    except:
                        inDyn.setData(inDyn.defaultValue())

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('StringPin')
        return helper

    @staticmethod
    def category():
        return 'Cmd'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'combine opts to one cmd line'

    def compute(self, *args, **kwargs):
        cmd_line = ""
        for elem in self.orderedInputs.values():
            name = elem.name.lstrip(" ")
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
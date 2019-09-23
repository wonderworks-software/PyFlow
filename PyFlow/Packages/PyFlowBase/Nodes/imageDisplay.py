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
from blinker import Signal
import os


class imageDisplay(NodeBase):
    def __init__(self, name):
        super(imageDisplay, self).__init__(name)
        self.loadImage = Signal(str)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('path', 'StringPin')
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin', None)
        self.failed = self.createOutputPin("failed", 'ExecPin', None)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('StringPin')
        helper.addInputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'UI'

    @staticmethod
    def keywords():
        return ['image']

    @staticmethod
    def description():
        return "Loads image to node body. This is UI only node"

    def compute(self, *args, **kwargs):
        path = self.entity.getData()
        if os.path.exists(path):
            self.loadImage.send(path)
            self.outExec.call()
        else:
            self.failed.call()

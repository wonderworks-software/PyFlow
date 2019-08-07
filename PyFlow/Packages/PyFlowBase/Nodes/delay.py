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

import threading

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class delay(NodeBase):
    def __init__(self, name):
        super(delay, self).__init__(name)
        self.inp0 = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.delay = self.createInputPin('Delay(s)', 'FloatPin')
        self.delay.setDefaultValue(0.2)
        self.out0 = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.headerColor = FLOW_CONTROL_COLOR
        self._currentTimer = None

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Delayed call'

    def callAndReset(self):
        self.out0.call()
        self._currentTimer.cancel()
        del self._currentTimer
        self._currentTimer = None

    def compute(self, *args, **kwargs):
        if self._currentTimer is not None:
            return
        self._currentDelay = self.delay.getData()
        self._currentTimer = threading.Timer(self._currentDelay, self.callAndReset)
        self._currentTimer.start()

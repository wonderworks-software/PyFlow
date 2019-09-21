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
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


## Timer node
class timer(NodeBase):
    def __init__(self, name):
        super(timer, self).__init__(name)
        self.out = self.createOutputPin("OUT", 'ExecPin')
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.interval = self.createInputPin("Delta(s)", 'FloatPin')
        self.interval.setDefaultValue(0.2)
        self.accum = 0.0
        self.bWorking = False
        self.headerColor = FLOW_CONTROL_COLOR

    def Tick(self, delta):
        super(timer, self).Tick(delta)
        if self.bWorking:
            interval = self.interval.getData()
            if interval < 0.02:
                interval = 0.02
            self.accum += delta
            if self.accum >= interval:
                self.out.call()
                self.accum = 0.0

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.accum = 0.0

    def start(self, *args, **kwargs):
        self.accum = 0.0
        self.bWorking = True

    @staticmethod
    def category():
        return 'FlowControl'

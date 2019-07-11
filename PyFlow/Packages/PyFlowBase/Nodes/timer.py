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
        self.resetPin = self.createInputPin("Reset", 'ExecPin', None, self.reset)
        self.interval = self.createInputPin("Delta(s)", 'FloatPin')
        self.interval.setDefaultValue(0.2)
        self.accum = 0.0
        self.bWorking = False
        self.headerColor = FLOW_CONTROL_COLOR

    def Tick(self, delta):
        super(timer, self).Tick(delta)
        if self.bWorking:
            interval = self.interval.getData()
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
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    def reset(self, *args, **kwargs):
        print("reset")

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.accum = 0.0

    def start(self, *args, **kwargs):
        self.accum = 0.0
        self.bWorking = True

    @staticmethod
    def category():
        return 'FlowControl'

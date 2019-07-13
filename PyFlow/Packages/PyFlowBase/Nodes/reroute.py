from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class reroute(NodeBase):
    def __init__(self, name):
        super(reroute, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', structure=PinStructure.Multi, constraint="1", structConstraint="1")
        self.output = self.createOutputPin("out", 'AnyPin', structure=PinStructure.Multi, constraint="1", structConstraint="1")
        self.input.checkForErrors = False
        self.output.checkForErrors = False
        self.input.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.output.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        pinAffects(self.input, self.output)
        self.input.call = self.output.call

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Multi)
        return helper

    @staticmethod
    def category():
        return 'Common'

    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())

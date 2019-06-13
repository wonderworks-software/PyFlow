from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class dictKeys(NodeBase):
    def __init__(self, name):
        super(dictKeys, self).__init__(name)
        self.dict = self.createInputPin("dict", "AnyPin", {}, structure=PinStructure.Dict)
        self.dict.enableOptions(PinOptions.DictSupported)
        self.dict.onPinConnected.connect(self.dictConnected)

        self.keys = self.createOutputPin("keys", "AnyPin", [], structure=PinStructure.Array)

    def dictConnected(self, other):
        print(other)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Dict)
        helper.addOutputStruct(PinStructure.Array)
        return helper

    @staticmethod
    def category():
        return 'Common'

    @staticmethod
    def keywords():
        return ["keys"]

    @staticmethod
    def description():
        return 'Returns an array of dict keys.'

    def compute(self, *args, **kwargs):
        self.keys.setData(list(self.dict.getData().keys()))

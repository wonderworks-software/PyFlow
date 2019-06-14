from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class dictKeys(NodeBase):
    def __init__(self, name):
        super(dictKeys, self).__init__(name)
        self.dict = self.createInputPin("dict", "AnyPin", structure=PinStructure.Dict)
        self.dict.enableOptions(PinOptions.DictSupported)
        self.dict.onPinConnected.connect(self.dictConnected)
        self.dict.dictChanged.connect(self.dictChanged)
        self.keys = self.createOutputPin("keys", "AnyPin", structure=PinStructure.Array)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

    def dictConnected(self, other):
        self.keys.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.keys.initType(other._data.keyType,True)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

    def dictChanged(self,dataType):
        self.keys.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.keys.initType(dataType,True)
        self.keys.disableOptions(PinOptions.ChangeTypeOnConnection)

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

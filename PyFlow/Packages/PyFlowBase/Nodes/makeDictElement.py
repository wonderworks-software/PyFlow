from PyFlow import getHashableDataTypes
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeDictElement(NodeBase):
    def __init__(self, name):
        super(makeDictElement, self).__init__(name)
        self.bCacheEnabled = False
        self.key = self.createInputPin('key', 'AnyPin', structure=PinStructure.Single, constraint="1", supportedPinDataTypes=getHashableDataTypes())
        self.value = self.createInputPin('value', 'AnyPin', structure=PinStructure.Multi, constraint="2")
        self.value.enableOptions(PinOptions.AllowAny)
        self.outArray = self.createOutputPin('out', 'AnyPin', defaultValue=DictElement(), structure=PinStructure.Single, constraint="2")
        self.outArray.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.outArray.onPinConnected.connect(self.outPinConnected)
        self.outArray.onPinDisconnected.connect(self.outPinDisConnected)
        self.key.dataBeenSet.connect(self.dataBeenSet)
        self.value.dataBeenSet.connect(self.dataBeenSet)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'GenericTypes'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a Dict Element'

    def dataBeenSet(self, pin=None):
        try:
            self.outArray._data = DictElement(self.key.getData(), self.value.getData())
            self.checkForErrors()
        except:
            pass

    def outPinDisConnected(self, inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            if dictNode.KeyType in self.constraints[self.key.constraint]:
                self.constraints[self.key.constraint].remove(dictNode.KeyType)
            if self.key in dictNode.constraints[self.key.constraint]:    
                dictNode.constraints[self.key.constraint].remove(self.key)
        self.outPinConnected(self.outArray)

    def outPinConnected(self, inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            dataType = dictNode.KeyType.dataType
            if not self.key.checkFree([]):
                dataType = self.key.dataType
            if dictNode.KeyType not in self.constraints[self.key.constraint]:
                self.constraints[self.key.constraint].append(dictNode.KeyType)
            if self.key not in dictNode.constraints[self.key.constraint]:
                dictNode.constraints[self.key.constraint].append(self.key)
            for i in dictNode.constraints[self.key.constraint]:
                i.setType(dataType)

    def compute(self, *args, **kwargs):
        self.outArray.setData(DictElement(self.key.getData(), self.value.getData()))

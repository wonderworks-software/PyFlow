from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeDictElement(NodeBase):
    def __init__(self, name):
        super(makeDictElement, self).__init__(name)
        self.bCacheEnabled = False
        self.key = self.createInputPin('key', 'AnyPin', structure=PinStructure.Single, constraint="1")
        self.value = self.createInputPin('value', 'AnyPin', structure=PinStructure.Multi, constraint="2")
        self.value.enableOptions(PinOptions.AllowAny)
        self.outArray = self.createOutputPin('out', 'AnyPin',defaultValue=(), structure=PinStructure.Single,constraint="2")
        self.outArray.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSuported)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}

    @staticmethod
    def category():
        return 'Array'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a Dict Element'

    def compute(self, *args, **kwargs):
        self.outArray.setData(dictElement(self.key.getData(),self.value.getData()))

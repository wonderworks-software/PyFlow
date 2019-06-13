from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeDictElement(NodeBase):
    def __init__(self, name):
        super(makeDictElement, self).__init__(name)
        self.key = self.createInputPin('key', 'AnyPin', structure=PinStructure.Single, constraint="1")
        self.value = self.createInputPin('value', 'AnyPin', structure=PinStructure.Multi, constraint="2")
        
        self.outArray = self.createOutputPin('out', 'dictElementPin',defaultValue=(), structure=PinStructure.Single,constraint="2")


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
        self.outArray.setData((self.key.getData(),self.value.getData()))

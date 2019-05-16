from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class address(NodeBase):
    def __init__(self, name):
        super(address, self).__init__(name)
        self.obj = self.createInputPin("obj", "AnyPin", structure=PinStructure.Multi)
        self.addr = self.createOutputPin('out', 'StringPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['StringPin']}

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return ['id']

    @staticmethod
    def description():
        return 'Returns address of an object in memory'

    def compute(self, *args, **kwargs):
        self.addr.setData(hex(id(self.obj.getData())))

from copy import deepcopy, copy

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class copyList(NodeBase):
    def __init__(self, name):
        super(copyList, self).__init__(name)
        self.entity = self.createInputPin('entity', 'AnyPin', constraint="1")
        self.entity.setAsList(True)

        self.deepcopy = self.createInputPin('deepcopy', 'BoolPin', False)
        self.copiedData = self.createOutputPin("copied", 'AnyPin', constraint="1")
        self.copiedData.setAsList(True)

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}

    @staticmethod
    def category():
        return 'DefaultLib'

    @staticmethod
    def keywords():
        return ['copy']

    @staticmethod
    def description():
        return "Shallow or deep copy of an object"

    def compute(self, *args, **kwargs):
        copyFunction = deepcopy if self.deepcopy.getData() else copy
        data = copyFunction(self.entity.getData())
        self.copiedData.setData(data)

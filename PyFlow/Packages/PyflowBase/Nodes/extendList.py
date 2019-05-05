from copy import deepcopy, copy

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import PinDirection


class extendList(NodeBase):
    def __init__(self, name):
        super(extendList, self).__init__(name)
        self.arrayA = self.createInputPin('first', 'AnyPin', constraint="1")
        self.arrayA.setAsList(True)
        self.arrayA.isArrayByDefault = True
        self.arrayA.supportsOnlyList = True

        self.arrayB = self.createInputPin('second', 'AnyPin', constraint="1")
        self.arrayB.setAsList(True)
        self.arrayB.isArrayByDefault = True
        self.arrayB.supportsOnlyList = True

        self.deepCopy = self.createInputPin('deepcopy', 'BoolPin', False)

        self.resultArray = self.createOutputPin('result', 'AnyPin', constraint="1")
        self.resultArray.setAsList(True)
        self.resultArray.isArrayByDefault = True
        self.resultArray.supportsOnlyList = True

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin'], 'outputs': ['AnyPin']}

    @staticmethod
    def category():
        return 'List'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates an list from connected pins'

    def compute(self, *args, **kwargs):
        bDeepCopy = self.deepCopy.getData()
        copyFunction = deepcopy if bDeepCopy else copy
        first = copyFunction(self.arrayA.getData())
        second = self.arrayB.getData()
        first.extend(second)
        self.resultArray.setData(first)

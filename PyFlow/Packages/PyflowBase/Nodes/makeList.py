from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeList(NodeBase):
    def __init__(self, name):
        super(makeList, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'AnyPin', constraint="1")
        self.arrayData.setAsList(True)
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyList)
        self.arrayData.changeTypeOnConnection = False

        self.sorted = self.createInputPin('sorted', 'BoolPin')
        self.reversed = self.createInputPin('reversed', 'BoolPin')
        self.outArray = self.createOutputPin('out', 'AnyPin', constraint="1")
        self.outArray.setAsList(True)
        self.outArray.changeTypeOnConnection = False

        self.result = self.createOutputPin('result', 'BoolPin')

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
        return 'Creates a list from connected pins'

    def compute(self, *args, **kwargs):
        outArray = []
        for i in self.arrayData.affected_by:
            outArray.append(i.getData())

        isSorted = self.sorted.getData()
        isReversed = self.reversed.getData()

        # not every type can be sorted
        try:
            if isSorted:
                outArray = list(sorted(outArray))
        except:
            self.result.setData(False)
            return

        if isReversed:
            outArray = list(reversed(outArray))

        self.outArray.setData(outArray)
        self.arrayData._data = outArray
        self.result.setData(True)

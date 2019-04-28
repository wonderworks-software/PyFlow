from PyFlow.Core import NodeBase
from PyFlow.Core.Common import PinDirection


class makeList(NodeBase):
    def __init__(self, name):
        super(makeList, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'AnyPin', constraint="1")
        self.arrayData.isArrayByDefault = True
        self.arrayData.setAsArray(True)
        # We want to populate array from all connected pins
        self.arrayData.supportsOnlyArray = False
        self.sorted = self.createInputPin('sorted', 'BoolPin')
        self.reversed = self.createInputPin('reversed', 'BoolPin')
        self.outArray = self.createOutputPin('out', 'AnyPin', constraint="1")
        self.outArray.isArrayByDefault = True
        self.outArray.setAsArray(True)
        self.outArray.supportsOnlyArray = True

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
        return 'Creates an array from connected pins'

    def compute(self, *args, **kwargs):
        outArray = []
        for i in self.arrayData.affected_by:
            outArray.append(i.getData())

        isSorted = self.sorted.getData()
        isReversed = self.reversed.getData()

        if isSorted:
            outArray = sorted(outArray)

        if isReversed:
            outArray = reversed(outArray)

        self.outArray.setData(outArray)
        self.arrayData._data = outArray

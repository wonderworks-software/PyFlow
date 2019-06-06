from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeList(NodeBase):
    def __init__(self, name):
        super(makeList, self).__init__(name)
        self.listData = self.createInputPin('data', 'AnyPin')
        self.listData.enableOptions(PinOptions.AllowMultipleConnections)
        self.listData.enableOptions(PinOptions.ArraySupported)
        self.listData.disableOptions(PinOptions.SupportsOnlyArrays)
        self.listData.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.sorted = self.createInputPin('sorted', 'BoolPin')
        self.reversed = self.createInputPin('reversed', 'BoolPin')
        self.outList = self.createOutputPin('out', 'AnyPin',structure=PinStructure.Array)
        self.outList.disableOptions(PinOptions.ChangeTypeOnConnection)

        self.result = self.createOutputPin('result', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ListPin'], 'outputs': ['ListPin']}

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
        outList = []
        for i in sorted(self.listData.affected_by, key=lambda pin: pin.owningNode().y):
            outList.append(i.getData())

        isSorted = self.sorted.getData()
        isReversed = self.reversed.getData()

        # not every type can be sorted
        try:
            if isSorted:
                outList = list(sorted(outList))
        except:
            self.result.setData(False)
            return

        if isReversed:
            outList = list(reversed(outList))

        self.outList.setData(outList)
        self.listData._data = outList
        self.result.setData(True)

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeArray(NodeBase):
    def __init__(self, name):
        super(makeArray, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'AnyPin', structure=PinStructure.Array, constraint="1")
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        self.sorted = self.createInputPin('sorted', 'BoolPin')
        self.reversed = self.createInputPin('reversed', 'BoolPin')
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Array, constraint="1")

        self.result = self.createOutputPin('result', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('AnyPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(PinStructure.Array)
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Array)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'Array'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a list from connected pins'

    def compute(self, *args, **kwargs):
        outArray = []
        ySortedPins = sorted(self.arrayData.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            if isinstance(i.getData(), list):
                for e in i.getData():
                    outArray.append(e)
            else:
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
        self.arrayData.setData(outArray)
        self.result.setData(True)

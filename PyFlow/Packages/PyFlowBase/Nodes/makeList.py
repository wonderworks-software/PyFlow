from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeList(NodeBase):
    def __init__(self, name):
        super(makeList, self).__init__(name)
        self.listData = self.createInputPin('data', 'AnyPin', structure=PinStructure.Array)
        self.listData.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.DictElementSupported | PinOptions.AllowAny)
        self.listData.disableOptions(PinOptions.ChangeTypeOnConnection | PinOptions.SupportsOnlyArrays)

        self.sorted = self.createInputPin('sorted', 'BoolPin')
        self.reversed = self.createInputPin('reversed', 'BoolPin')
        self.outList = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Array)
        self.outList.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.outList.enableOptions(PinOptions.AllowAny)

        self.result = self.createOutputPin('result', 'BoolPin')
        self.checkForErrors()

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
        return 'GenericTypes'

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

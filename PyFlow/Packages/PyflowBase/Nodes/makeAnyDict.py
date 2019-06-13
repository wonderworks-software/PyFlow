from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeAnyDict(NodeBase):
    def __init__(self, name):
        super(makeAnyDict, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'AnyPin', structure=PinStructure.Dict, constraint="1")
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSuported)
        self.arrayData.disableOptions(PinOptions.ChangeTypeOnConnection | PinOptions.SupportsOnlyArrays)
        self.arrayData.disableOptions()
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Dict, constraint="1")
        self.outArray.enableOptions(PinOptions.AllowAny)
        self.outArray.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.result = self.createOutputPin('result', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Dict)
        helper.addOutputStruct(PinStructure.Dict)
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
        outArray = {}
        ySortedPins = sorted(self.arrayData.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            if isinstance(i.getData(), dictElement):
                outArray[i.getData()[0]] = i.getData()[1]

        self.outArray.setData(outArray)
        self.arrayData.setData(outArray)
        self.result.setData(True)

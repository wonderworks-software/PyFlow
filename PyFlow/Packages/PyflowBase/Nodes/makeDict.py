from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeDict(NodeBase):
    def __init__(self, name):
        super(makeDict, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'dictElementPin', structure=PinStructure.Dict, constraint="1")
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)

        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Dict, constraint="1")

        self.result = self.createOutputPin('result', 'BoolPin')

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
        return 'Creates a list from connected pins'

    def compute(self, *args, **kwargs):
        outArray = {}
        ySortedPins = sorted(self.arrayData.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            if isinstance(i.getData(), tuple) and len(i.getData())==2:
                outArray[i.getData()[0]] = i.getData()[1]


        self.outArray.setData(outArray)
        self.arrayData.setData(outArray)
        self.result.setData(True)

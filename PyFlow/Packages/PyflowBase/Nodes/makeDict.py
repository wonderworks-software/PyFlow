from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class makeDict(NodeBase):
    def __init__(self, name):
        super(makeDict, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'AnyPin', structure=PinStructure.Dict, constraint="1")
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSuported)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Dict, constraint="1")
        self.outArray.enableOptions(PinOptions.AllowAny)
        self.result = self.createOutputPin('result', 'BoolPin')
        self.arrayData.onPinDisconnected.connect(self.inPinDisconnected)
        self.arrayData.onPinConnected.connect(self.inPinConnected)

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
    
    def inPinConnected(self,inp):
        inp = inp.getDictElementNode([])
        if inp:
            for i in self.arrayData.affected_by:
                dictItem = i.getDictElementNode([])
                if dictItem:
                    if dictItem.key not in inp.constraints[inp.key.constraint]:
                        inp.constraints[inp.key.constraint].append(dictItem.key)
                    if inp.key not in dictItem.constraints[inp.key.constraint]:    
                        dictItem.constraints[inp.key.constraint].append(inp.key)
                    inp.key.setType(dictItem.key.dataType)      
    def inPinDisconnected(self,inp):
        inp = inp.getDictElementNode([])
        if inp:
            for i in self.arrayData.affected_by:
                dictItem = i.getDictElementNode([])
                if dictItem:
                    if dictItem.key in inp.constraints[inp.key.constraint]:
                        inp.constraints[inp.key.constraint].remove(dictItem.key)
                    if inp.key in dictItem.constraints[inp.key.constraint]:    
                        dictItem.constraints[inp.key.constraint].remove(inp.key)        

    def compute(self, *args, **kwargs):
        outArray = {}
        ySortedPins = sorted(self.arrayData.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            if isinstance(i.getData(), dictElement):
                outArray[i.getData()[0]] = i.getData()[1]

        self.outArray.setData(outArray)
        self.arrayData.setData(outArray)
        self.result.setData(True)

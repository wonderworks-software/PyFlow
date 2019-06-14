from PyFlow import _HASHABLES
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeDict(NodeBase):
    def __init__(self, name):
        super(makeDict, self).__init__(name)
        self.KeyType = self.createInputPin('KeyType', 'AnyPin',defaultValue=str(""), constraint="1",allowedPins=_HASHABLES)
        #self.KeyType.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.KeyType.hidden = True
        #self.ValueType = self.createInputPin('valueType', 'AnyPin', constraint="2")

        self.arrayData = self.createInputPin('data', 'AnyPin', structure=PinStructure.Dict, constraint="2")
        self.arrayData.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSuported)
        self.arrayData.disableOptions(PinOptions.SupportsOnlyArrays)
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Dict, constraint="2")
        self.outArray.enableOptions(PinOptions.AllowAny)
        self.result = self.createOutputPin('result', 'BoolPin')
        self.arrayData.onPinDisconnected.connect(self.inPinDisconnected)
        self.arrayData.onPinConnected.connect(self.inPinConnected)
        self.KeyType.typeChanged.connect(self.updateDicts)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(PinStructure.Dict)
        helper.addOutputStruct(PinStructure.Dict)
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

    def updateDicts(self,dataType):
        self.arrayData.updateConectedDicts([],self.KeyType.dataType)

    def inPinConnected(self,inp):
        inp = inp.getDictElementNode([])
        if inp:
            if self.KeyType not in inp.constraints[inp.key.constraint]:
                inp.constraints[inp.key.constraint].append(self.KeyType)
            if inp.key not in self.constraints[inp.key.constraint]:    
                self.constraints[inp.key.constraint].append(inp.key)
            inp.key.setType(self.KeyType.dataType)

            #if self.ValueType not in inp.constraints[inp.value.constraint]:
            #    inp.constraints[inp.value.constraint].append(self.ValueType)
            #if inp.value not in self.constraints[inp.value.constraint]:    
            #    self.constraints[inp.value.constraint].append(inp.value)
            #inp.value.setType(self.ValueType.dataType)

    def inPinDisconnected(self,inp):
        inp = inp.getDictElementNode([])
        elements = [i.getDictElementNode([]) for i in self.arrayData.affected_by]
        if inp is not None :
            if self.KeyType in inp.constraints[inp.key.constraint]:
                inp.constraints[inp.key.constraint].remove(self.KeyType)
            if inp.key in self.constraints[inp.key.constraint]:    
                self.constraints[inp.key.constraint].remove(inp.key)

            #if self.ValueType in inp.constraints[inp.value.constraint]:
            #    inp.constraints[inp.value.constraint].remove(self.ValueType)
            #if inp.value in self.constraints[inp.value.constraint]:    
            #    self.constraints[inp.value.constraint].remove(inp.value)  
            #inp.outPinConnected(inp.outArray)

    def compute(self, *args, **kwargs):
        outArray = pyf_dict(self.KeyType.dataType)
        ySortedPins = sorted(self.arrayData.affected_by, key=lambda pin: pin.owningNode().y)

        for i in ySortedPins:
            if isinstance(i.getData(), dictElement):
                outArray[i.getData()[0]] = i.getData()[1]
            elif isinstance(i.getData(), pyf_dict):
                for key,value in i.getData().items():
                    outArray[key] = value

        self.outArray.setData(outArray)
        self.arrayData.setData(outArray)
        self.result.setData(True)

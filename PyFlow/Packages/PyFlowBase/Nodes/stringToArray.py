from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import ast

class stringToArray(NodeBase):
    def __init__(self, name):
        super(stringToArray, self).__init__(name)
        self.arrayData = self.createInputPin('data', 'StringPin', structure=PinStructure.Single)
        self.outArray = self.createOutputPin('out', 'AnyPin', structure=PinStructure.Array)
        self.result = self.createOutputPin('result', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('StringPin')
        helper.addOutputDataType('AnyPin')
        helper.addOutputDataType('BoolPin')
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
        return 'Creates a list from ast.literal_eval(data) and then converts to output DataType'

    def compute(self, *args, **kwargs):
        outArray = []
        stringData = "[%s]"%self.arrayData.getData()
        if self.outArray.dataType == "AnyPin":
            self.outArray.setData(outArray)
            self.result.setData(False)
        else:
            splited = ast.literal_eval(stringData)
            for i in splited:
                processedData = self.outArray.super.processData(i)
                outArray.append(processedData)
            self.outArray.setData(outArray)
            self.result.setData(True)

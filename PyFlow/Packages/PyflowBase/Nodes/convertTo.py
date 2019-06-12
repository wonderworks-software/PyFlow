from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow import CreateRawPin
from copy import copy
from multipledispatch import dispatch

class convertTo(NodeBase):
    def __init__(self, name):
        super(convertTo, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin',defaultValue=None)
        self.output = self.createOutputPin("result", 'AnyPin',defaultValue=None)
        pinAffects(self.input, self.output)
        #self.input.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.input.enableOptions(PinOptions.AllowAny)
        self.pinTypes = []
        for pinClass in getAllPinClasses():
            if pinClass.IsValuePin():
                self.pinTypes.append(pinClass.__name__ )
        self.bCacheEnabled = False

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'         

    def updateType(self,dataTypeIndex):
        self.output.enableOptions(PinOptions.ChangeTypeOnConnection)        
        self.changeType(self.pinTypes[dataTypeIndex],True)
        self.output.disableOptions(PinOptions.ChangeTypeOnConnection)  
     
    def changeType(self,dataType,init=False):
        b = self.output.initType(dataType,init)

    def compute(self, *args, **kwargs):
        otherClass = findPinClassByType(self.output.dataType)
        self.output.setData(otherClass.processData(self.input.getData()))

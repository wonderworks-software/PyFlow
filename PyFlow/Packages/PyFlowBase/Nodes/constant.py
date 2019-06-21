from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow import CreateRawPin
from copy import copy
from multipledispatch import dispatch

class constant(NodeBase):
    def __init__(self, name):
        super(constant, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', defaultValue=0.0, structure=PinStructure.Multi, constraint="1", structConstraint="1")
        self.output = self.createOutputPin("out", 'AnyPin', defaultValue=0.0, structure=PinStructure.Multi, constraint="1", structConstraint="1")
        pinAffects(self.input, self.output)
        self.input.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.output.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.input.call = self.output.call
        self.pinTypes = []
        for pinClass in getAllPinClasses():
            if pinClass.IsValuePin() and pinClass.__name__ != "AnyPin":
                self.pinTypes.append(pinClass.__name__)
        self.bCacheEnabled = False

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Multi)
        return helper

    @staticmethod
    def category():
        return 'GenericTypes'
        
    @staticmethod
    def keywords():
        return ["Make"]

    def postCreate(self, jsonTemplate=None):
        super(constant, self).postCreate(jsonTemplate)
        self.input.onPinConnected.connect(self.onPinConected)
        self.output.onPinConnected.connect(self.onPinConected)

    def onPinConected(self,other):
        self.changeType(other.dataType)

    def overrideTypeChanged(self,toogle):
        if bool(toogle):
            self.input.enableOptions(PinOptions.ChangeTypeOnConnection)
            self.output.enableOptions(PinOptions.ChangeTypeOnConnection)
        else:
            self.input.disableOptions(PinOptions.ChangeTypeOnConnection)
            self.output.disableOptions(PinOptions.ChangeTypeOnConnection)            

    def updateType(self,dataTypeIndex):
        self.input.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.output.enableOptions(PinOptions.ChangeTypeOnConnection)        
        self.changeType(self.pinTypes[dataTypeIndex],True)
        self.input.disableOptions(PinOptions.ChangeTypeOnConnection)
        self.output.disableOptions(PinOptions.ChangeTypeOnConnection)  
     
    def changeType(self,dataType,init=False):
        a = self.input.initType(dataType,init)
        b = self.output.initType(dataType,init)

    def selectStructure(self,name):
        self.input.changeStructure(PinStructure(name),True)
        self.output.changeStructure(PinStructure(name),True)


    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())

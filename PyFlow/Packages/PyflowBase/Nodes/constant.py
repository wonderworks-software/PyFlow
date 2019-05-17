from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow import CreateRawPin
from copy import copy
from multipledispatch import dispatch

class constant(NodeBase):
    def __init__(self, name):
        super(constant, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', structure=PinStructure.Multi, constraint="1",structConstraint="1")
        self.output = self.createOutputPin("out", 'AnyPin', structure=PinStructure.Multi, constraint="1",structConstraint="1")
        #self.input.typeChanged.connect(self.changeType)
        #self.output.typeChanged.connect(self.changeType)

        pinAffects(self.input, self.output)
        self.input.call = self.output.call
        self.pinTypes = []
        for pinClass in getAllPinClasses():
            self.pinTypes.append(pinClass.__name__ )

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return 'Common'

    def postCreate(self, jsonTemplate=None):
        super(constant, self).postCreate(jsonTemplate)
        self.input.onPinConnected.connect(self.onPinConected)
        self.output.onPinConnected.connect(self.onPinConected)

    def onPinConected(self,other):
        self.changeType(other.dataType)

    def updateType(self,dataTypeIndex):
        self.changeType(self.pinTypes[dataTypeIndex])

    def changeType(self,dataType):
        a = self.input.initType(dataType)
        b = self.output.initType(dataType)
        self._wrapper.changeType(dataType)


    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())

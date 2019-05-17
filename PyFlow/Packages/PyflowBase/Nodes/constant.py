from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import findPinClassByType, getAllPinClasses
from PyFlow import CreateRawPin
from copy import copy


class constant(NodeBase):
    def __init__(self, name):
        super(constant, self).__init__(name)
        self.input = self.createInputPin("in", 'AnyPin', structure=PinStructure.Multi, constraint="1",structConstraint="1")
        self.output = self.createOutputPin("out", 'AnyPin', structure=PinStructure.Multi, constraint="1",structConstraint="1")
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

    def changeType(self,dataType):
        self.input.initType(self.pinTypes[dataType])
        self.output.initType(self.pinTypes[dataType])

    def compute(self, *args, **kwargs):
        self.output.setData(self.input.getData())

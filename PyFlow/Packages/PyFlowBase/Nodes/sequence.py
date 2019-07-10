from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class sequence(NodeBase):
    def __init__(self, name):
        super(sequence, self).__init__(name)
        self.inExecPin = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.headerColor = FLOW_CONTROL_COLOR

    def createOutputPin(self, *args, **kwargs):
        pinName = str(len(self.outputs) + 1)
        p = CreateRawPin(pinName, self, 'ExecPin', PinDirection.Output)
        p.enableOptions(PinOptions.Dynamic)
        return p

    def serialize(self):
        data = super(sequence, self).serialize()
        data['numOutputs'] = len(self.outputs)
        return data

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    def postCreate(self, jsonTemplate=None):
        super(sequence, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamic pins
        if jsonTemplate is not None and 'numOutputs' in jsonTemplate:
            for i in range(jsonTemplate['numOutputs']):
                self.createOutputPin()

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'The Sequence node allows for a single execution pulse to trigger a series of events in order. The node may have any number of outputs, all of which get called as soon as the Sequence node receives an input. They will always get called in order, but without any delay. To a typical user, the outputs will likely appear to have been triggered simultaneously.'

    def compute(self, *args, **kwargs):
        for out in self.outputs.values():
            out.call(*args, **kwargs)

from PyFlow import CreateRawPin
from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class sequence(NodeBase):
    def __init__(self, name):
        super(sequence, self).__init__(name)
        self.inExecPin = self.createInputPin('inExec', 'ExecPin', None, self.compute)

    def createOutputPin(self, *args, **kwargs):
        currentIds = [int(i) for i in self.namePinOutputsMap]
        pinName = str(findGoodId(currentIds)) if 'name' not in kwargs else kwargs['name']
        p = CreateRawPin(pinName, self, 'ExecPin', PinDirection.Output)
        return p

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    def postCreate(self, jsonTemplate=None):
        super(sequence, self).postCreate(jsonTemplate=jsonTemplate)
        # recreate dynamic pins
        if jsonTemplate is not None:
            for outJson in jsonTemplate['outputs']:
                if outJson['name'] not in self.namePinOutputsMap:
                    pin = self.createOutputPin(outJson['name'])

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'The Sequence node allows for a single execution pulse to trigger a series of events in order. The node may have any number of outputs, all of which get called as soon as the Sequence node receives an input. They will always get called in order, but without any delay. To a typical user, the outputs will likely appear to have been triggered simultaneously.'

    def compute(self, *args, **kwargs):
        for out in self.outputs.values():
            out.call(*args, **kwargs)

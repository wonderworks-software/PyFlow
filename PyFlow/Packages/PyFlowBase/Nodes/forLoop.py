from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class forLoop(NodeBase):
    def __init__(self, name):
        super(forLoop, self).__init__(name)
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.firstIndex = self.createInputPin('Start', 'IntPin')
        self.lastIndex = self.createInputPin('Stop', 'IntPin')
        self.step = self.createInputPin('Step', 'IntPin')
        self.step.setData(1)

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.index = self.createOutputPin('Index', 'IntPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.headerColor = FLOW_CONTROL_COLOR

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('IntPin')
        helper.addOutputDataType('ExecPin')
        helper.addOutputDataType('IntPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop'

    def compute(self, *args, **kwargs):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        if step == 0:
            self.completed.call(*args, **kwargs)
        else:
            for i in range(indexFrom, indexTo, step):
                self.index.setData(i)
                push(self.index)
                self.loopBody.call(*args, **kwargs)
            self.completed.call(*args, **kwargs)

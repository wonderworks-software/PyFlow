from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class forLoopWithBreak(NodeBase):
    def __init__(self, name):
        super(forLoopWithBreak, self).__init__(name)
        self.stop = False
        self.inExec = self.createInputPin('inExec', 'ExecPin', None, self.compute)
        self.firstIndex = self.createInputPin('Start', 'IntPin')
        self.lastIndex = self.createInputPin('Stop', 'IntPin')
        self.lastIndex.setDefaultValue(10)
        self.step = self.createInputPin('Step', 'IntPin')
        self.step.setDefaultValue(1)
        self.breakExec = self.createInputPin('Break', 'ExecPin', None, self.interrupt)

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

    def interrupt(self, *args, **kwargs):
        self.stop = True

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter']

    @staticmethod
    def description():
        return 'For loop with ability to break'

    def compute(self, *args, **kwargs):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        for i in range(indexFrom, indexTo, step):
            if self.stop:
                break
            self.index.setData(i)
            self.loopBody.call(*args, **kwargs)
        self.completed.call(*args, **kwargs)
        self.stop = False

from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class forEachLoop(NodeBase):
    def __init__(self, name):
        super(forEachLoop, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.array = self.createInputPin('array', 'AnyPin', structure=PinStructure.Array, constraint="1")
        self.array.enableOptions(PinOptions.AllowAny)

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.elem = self.createOutputPin('element', 'AnyPin', constraint="1")
        self.elem.enableOptions(PinOptions.AllowAny)
        self.completed = self.createOutputPin('Completed', 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['AnyPin', 'ExecPin'], 'outputs': ['ExecPin', 'AnyPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return ['iter', 'for', 'loop', 'each']

    @staticmethod
    def description():
        return 'For each loop'

    def compute(self, *args, **kwargs):
        ls = self.array.getData()
        if len(ls) == 0:
            self.completed.call(*args, **kwargs)
        else:
            for i in ls:
                self.elem.setData(i)
                push(self.elem)
                self.loopBody.call(*args, **kwargs)
            self.completed.call(*args, **kwargs)

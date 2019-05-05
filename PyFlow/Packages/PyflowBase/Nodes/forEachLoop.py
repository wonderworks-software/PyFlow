from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *


class forEachLoop(NodeBase):
    def __init__(self, name):
        super(forEachLoop, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.list = self.createInputPin('list', 'AnyPin', constraint="1")
        self.list.setAsList(True)
        self.list.arraySupported = True
        self.list.isArrayByDefault = True

        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.elem = self.createOutputPin('element', 'AnyPin', constraint="1")
        self.elem.setAsList(False)
        self.elem.listSwitchPolicy = ListSwitchPolicy.DoNotSwitch
        self.elem.arraySupported = False
        self.elem.isArrayByDefault = False
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
        ls = self.list.getData()
        if len(ls) == 0:
            self.completed.call(*args, **kwargs)
        else:
            for i in ls:
                self.elem.setData(i)
                push(self.elem)
                self.loopBody.call(*args, **kwargs)
            self.completed.call(*args, **kwargs)

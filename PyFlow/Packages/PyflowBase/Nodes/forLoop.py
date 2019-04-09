from PyFlow.Core import NodeBase
from PyFlow.Core.Common import push


class forLoop(NodeBase):
    def __init__(self, name, parent):
        super(forLoop, self).__init__(name)
        self.inExec = self.addInputPin('inExec', 'ExecPin', None, self.compute)
        self.firstIndex = self.addInputPin('Start', 'IntPin')
        self.lastIndex = self.addInputPin('Stop', 'IntPin')
        self.step = self.addInputPin('Step', 'IntPin')
        self.step.setData(1)

        self.loopBody = self.addOutputPin('LoopBody', 'ExecPin')
        self.index = self.addOutputPin('Index', 'IntPin')
        self.completed = self.addOutputPin('Completed', 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'IntPin'], 'outputs': ['ExecPin', 'IntPin']}

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

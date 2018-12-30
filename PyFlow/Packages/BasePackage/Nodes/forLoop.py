from PyFlow.Core import NodeBase


class forLoop(NodeBase):
    def __init__(self, name, graph):
        super(forLoop, self).__init__(name, graph)
        self.inExec = self.addInputPin('inExec', 'ExecPin', self.compute)
        self.firstIndex = self.addInputPin('Start', 'IntPin')
        self.lastIndex = self.addInputPin('Stop', 'IntPin')
        self.step = self.addInputPin('Step', 'IntPin')
        self.step.setData(1)

        self.loopBody = self.addOutputPin('LoopBody', 'ExecPin')
        self.index = self.addOutputPin('Index', 'IntPin')
        self.completed = self.addOutputPin('Completed', 'ExecPin')

        pinAffects(self.firstIndex, self.index)
        pinAffects(self.lastIndex, self.index)
        pinAffects(self.step, self.index)

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

    def compute(self):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        if step == 0:
            self.completed.call()
        else:
            for i in range(indexFrom, indexTo, step):
                self.index.setData(i)
                self.loopBody.call()
            self.completed.call()

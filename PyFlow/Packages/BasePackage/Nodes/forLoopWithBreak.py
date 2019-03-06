from PyFlow.Core import NodeBase


class forLoopWithBreak(NodeBase):
    def __init__(self, name):
        super(forLoopWithBreak, self).__init__(name)
        self.stop = False
        self.inExec = self.addInputPin('inExec', 'ExecPin', None, self.compute)
        self.firstIndex = self.addInputPin('Start', 'IntPin')
        self.lastIndex = self.addInputPin('Stop', 'IntPin')
        self.lastIndex.setDefaultValue(10)
        self.step = self.addInputPin('Step', 'IntPin')
        self.step.setDefaultValue(1)
        self.breakExec = self.addInputPin('Break', 'ExecPin', None, self.interrupt)

        self.loopBody = self.addOutputPin('LoopBody', 'ExecPin')
        self.index = self.addOutputPin('Index', 'IntPin')
        self.completed = self.addOutputPin('Completed', 'ExecPin')

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['ExecPin', 'IntPin'], 'outputs': ['ExecPin', 'IntPin']}

    def interrupt(self):
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

    def compute(self):
        indexFrom = self.firstIndex.getData()
        indexTo = self.lastIndex.getData()
        step = self.step.getData()
        for i in range(indexFrom, indexTo, step):
            if self.stop:
                break
            self.index.setData(i)
            self.loopBody.call()
        self.completed.call()
        self.stop = False

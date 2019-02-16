from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase


class whileLoop(NodeBase):
    def __init__(self, name):
        super(whileLoop, self).__init__(name)
        self.inExec = self.addInputPin('inExec', 'ExecPin', self.begin)
        self.bCondition = self.addInputPin('Condition', 'BoolPin')
        self.loopBody = self.addOutputPin('LoopBody', 'ExecPin')
        self.completed = self.addOutputPin('Completed', 'ExecPin')
        self.bProcess = False
        self._dirty = False

    @staticmethod
    def packageName():
        return PACKAGE_NAME

    def begin(self):
        self.bProcess = True

    @staticmethod
    def pinTypeHints():
        return {'inputs': ['BoolPin', 'ExecPin'], 'outputs': ['ExecPin']}

    @staticmethod
    def category():
        return 'FlowControl'

    @staticmethod
    def keywords():
        return []

    def Tick(self, deltaTime):
        currentCondition = self.bCondition.getData()

        if self.bProcess and currentCondition:
            self.loopBody.call()
            # when started mark dirty to call completed lated
            if not self._dirty:
                self._dirty = True
            return
        else:
            self.bProcess = False

        # of _dirty is True that means condition been changed from True to False
        # so in that case call completed and set clean
        if self._dirty:
            self.completed.call()
            self._dirty = False

    @staticmethod
    def description():
        return 'The WhileLoop node will output a result so long as a specific condition is true. During each iteration of the loop, it checks to see the current status of its input boolean value. As soon as it reads false, the loop breaks.\nAs with While loops in programming languages, extra care must be taken to prevent infinite loops from occurring.'

from ..Core.AbstractGraph import *
from ..Core.Settings import *
# from ..Core import Node


class whileLoop(NodeBase):
    def __init__(self, name):
        super(whileLoop, self).__init__(name)
        self.inExec = self.addInputPin('inExec', DataTypes.Exec, self.begin)
        self.bCondition = self.addInputPin('Condition', DataTypes.Bool)
        self.loopBody = self.addOutputPin('LoopBody', DataTypes.Exec)
        self.completed = self.addOutputPin('Completed', DataTypes.Exec)
        self.bProcess = False
        self._dirty = False

    def begin(self):
        self.bProcess = True

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Bool, DataTypes.Exec], 'outputs': [DataTypes.Exec]}

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

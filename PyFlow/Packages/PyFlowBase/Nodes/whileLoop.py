from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class whileLoop(NodeBase):
    def __init__(self, name):
        super(whileLoop, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.begin)
        self.bCondition = self.createInputPin('Condition', 'BoolPin')
        self.loopBody = self.createOutputPin('LoopBody', 'ExecPin')
        self.completed = self.createOutputPin('Completed', 'ExecPin')
        self.bProcess = False
        self._dirty = False
        self.headerColor = FLOW_CONTROL_COLOR

    def begin(self, *args, **kwargs):
        self.bProcess = True

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addOutputStruct(PinStructure.Single)
        return helper

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

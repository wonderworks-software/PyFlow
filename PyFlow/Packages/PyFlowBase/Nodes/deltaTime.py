from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class deltaTime(NodeBase):
    def __init__(self, name):
        super(deltaTime, self).__init__(name)
        self._deltaTime = 0.0
        self._out0 = self.createOutputPin('out0', 'FloatPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('FloatPin')
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Editor delta time.'

    def Tick(self, deltaTime):
        self._deltaTime = deltaTime

    def compute(self, *args, **kwargs):
        self._out0.setData(self._deltaTime)
        # TODO: cache previous value and push dirty only if value changed
        push(self._out0)

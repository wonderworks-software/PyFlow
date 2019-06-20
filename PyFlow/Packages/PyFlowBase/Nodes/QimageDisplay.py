from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

from Qt import QtGui

class QimageDisplay(NodeBase):
    def __init__(self, name):
        super(QimageDisplay, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('path', 'StringPin')
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin', None)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('StringPin')
        helper.addInputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'DefaultLib'

    @staticmethod
    def keywords():
        return ['image']

    @staticmethod
    def description():
        return "Python's 'print' function wrapper"

    def compute(self, *args, **kwargs):
        self.getWrapper().pixmap = QtGui.QPixmap(self.entity.getData())
        self.getWrapper().updateSize()
        self.outExec.call()

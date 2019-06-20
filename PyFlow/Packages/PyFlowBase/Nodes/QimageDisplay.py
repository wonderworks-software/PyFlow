from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from blinker import Signal
import os


class QimageDisplay(NodeBase):
    def __init__(self, name):
        super(QimageDisplay, self).__init__(name)
        self.loadImage = Signal(str)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.entity = self.createInputPin('path', 'StringPin')
        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin', None)
        self.failed = self.createOutputPin("Failed", 'ExecPin', None)

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
        return "Loads image to node body. This is UI only node"

    def compute(self, *args, **kwargs):
        path = self.entity.getData()
        if os.path.exists(path):
            self.loadImage.send(path)
            self.outExec.call()
        else:
            self.failed.call()

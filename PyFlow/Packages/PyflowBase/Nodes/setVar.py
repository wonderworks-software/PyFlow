from copy import copy

from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin
import uuid


class setVar(NodeBase):
    def __init__(self, name, var=None):
        super(setVar, self).__init__(name)
        self.inExec = self.addInputPin('exec', 'ExecPin', None, self.compute)
        self.outExec = self.addOutputPin('exec', 'ExecPin')
        self.var = var
        self.inp = CreateRawPin("inp", self, self.var.dataType, PinDirection.Input)
        self.out = CreateRawPin("out", self, self.var.dataType, PinDirection.Output)

    def serialize(self):
        default = NodeBase.serialize(self)
        default['varUid'] = str(self.var.uid)
        return default

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return PACKAGE_NAME

    @staticmethod
    def keywords():
        return ["set", "var"]

    @staticmethod
    def description():
        return 'Set variable value'

    def compute(self, *args, **kwargs):
        newValue = self.inp.getData()
        self.var.value = newValue
        self.out.setData(copy(self.var.value))
        self.outExec.call(*args, **kwargs)

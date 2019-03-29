from copy import copy
import uuid

from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Variable import Variable
from PyFlow.Core.Common import *
from PyFlow import CreateRawPin


class getVar(NodeBase):
    def __init__(self, name, var=None):
        super(getVar, self).__init__(name)
        assert(isinstance(var, Variable))
        self.varUid = var.uid
        self.var = var
        self.out = CreateRawPin('value', self, var.dataType, PinDirection.Output)
        self.var.valueChanged.connect(self.onVarValueChanged)
        self.var.killed.connect(self.kill)

    def recreateOutput(self, dataType):
        self.out.kill()
        del self.out
        self.out = None
        self.out = CreateRawPin('value', self, dataType, PinDirection.Output)
        return True

    def onVarValueChanged(self, *args, **kwargs):
        push(self.out)

    def serialize(self):
        default = NodeBase.serialize(self)
        default['varUid'] = str(self.varUid)
        return default

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    @staticmethod
    def category():
        return PACKAGE_NAME

    @staticmethod
    def keywords():
        return ["get", "var"]

    @staticmethod
    def description():
        return 'Access variable value'

    def compute(self, *args, **kwargs):
        var = self.graph().vars[self.varUid]
        self.out.setData(copy(var.value))

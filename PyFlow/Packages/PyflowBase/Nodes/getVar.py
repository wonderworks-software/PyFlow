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
        self._var = var
        self.out = self.createOutputPin('value', "AnyPin")
        self.out.disableOptions(PinOptions.RenamingEnabled)

        self._var.valueChanged.connect(self.onVarValueChanged)
        self.bCacheEnabled = False

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, newVar):
        self._var.valueChanged.disconnect(self.onVarValueChanged)
        self._var = newVar
        self._var.valueChanged.connect(self.onVarValueChanged)
        self.out.disconnectAll()
        self.out.setType(self._var.dataType)

    def postCreate(self, jsonTemplate=None):
        super(getVar, self).postCreate(jsonTemplate)
        self.out.setType(self.var.dataType)

    def variableUid(self):
        return self.var.uid

    def onVarValueChanged(self, *args, **kwargs):
        push(self.out)

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
        return ["get", "var"]

    @staticmethod
    def description():
        return 'Access variable value'

    def compute(self, *args, **kwargs):
        self.out.setData(copy(self.var.value))

from copy import copy

from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase
import uuid


class setVar(NodeBase):
    def __init__(self, name):
        super(setVar, self).__init__(name)
        self.inExec = self.addInputPin('exec', 'ExecPin', None, self.compute)
        self.outExec = self.addOutputPin('exec', 'ExecPin')
        self.var = None
        self.inp = None
        self.out = None

    def postCreate(self, jsonTemplate=None):
        super(setVar, self).postCreate(jsonTemplate)

        varUid = uuid.UUID(jsonTemplate['meta']['var']['uuid'])
        self.var = self.graph().vars[varUid]

        self.inp = self.addInputPin('inp', self.var.dataType)
        self.out = self.addOutputPin('out', self.var.dataType)
        self.graph().pins[self.inp.uid] = self.inp
        self.graph().pins[self.out.uid] = self.out

    @staticmethod
    def packageName():
        return PACKAGE_NAME

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

    def compute(self):
        newValue = self.inp.getData()
        self.var.value = newValue
        self.out.setData(copy(self.var.value))
        self.outExec.call()

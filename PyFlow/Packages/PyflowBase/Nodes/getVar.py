from copy import copy

from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
import uuid


class getVar(NodeBase):
    def __init__(self, name):
        super(getVar, self).__init__(name)
        self.var = None
        self.out = None

    def postCreate(self, jsonTemplate=None):
        super(getVar, self).postCreate(jsonTemplate)

        varUid = uuid.UUID(jsonTemplate['meta']['var']['uuid'])
        self.var = self.graph().vars[varUid]

        self.out = self.addOutputPin('val', self.var.dataType)
        self.graph().pins[self.out.uid] = self.out

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

    def compute(self):
        self.out.setData(copy(self.var.value))

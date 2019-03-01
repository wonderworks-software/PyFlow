from copy import copy

from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase


class getVar(NodeBase):
    def __init__(self, name):
        super(getVar, self).__init__(name)
        self.var = None
        # self.out = self.addOutputPin('value', self.var.dataType)

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
        return ["get", "var"]

    @staticmethod
    def description():
        return 'Access variable value'

    def compute(self):
        # self._out0.setData(copy(self.var.value))
        pass

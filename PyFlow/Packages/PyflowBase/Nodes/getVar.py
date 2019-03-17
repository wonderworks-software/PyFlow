from copy import copy
import uuid

from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import NodeBase
from PyFlow.Core.Common import push


class getVar(NodeBase):
    def __init__(self, name, varUid=None):
        super(getVar, self).__init__(name)
        assert(isinstance(varUid, uuid.UUID))
        self.varUid = varUid
        self.out = self.addOutputPin('val', 'AnyPin')

    def postCreate(self, jsonTemplate=None):
        super(getVar, self).postCreate(jsonTemplate=jsonTemplate)
        # var already created and uid is saved in constructor
        # connect to data changed event and dirty propagate the graph
        assert(self.varUid in self.graph().vars), "var {0} is not in graph {1}".format(
            str(self.varUid), self.graph().name)
        self.graph().vars[self.varUid].valueChanged.connect(
            self.onVarValueChanged)

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

    def compute(self):
        var = self.graph().vars[self.varUid]
        self.out.setData(copy(var.value))

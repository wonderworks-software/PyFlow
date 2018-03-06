from ..Core.AbstractGraph import *
from ..Core.Settings import *
from ..Core import Node


## If else node
class branch(Node, NodeBase):
    def __init__(self, name, graph):
        super(branch, self).__init__(name, graph)
        self.trueExec = self.addOutputPin("True", DataTypes.Exec)
        self.falseExec = self.addOutputPin("False", DataTypes.Exec)
        self.inExec = self.addInputPin("In", DataTypes.Exec, self.compute, hideLabel=True)
        self.condition = self.addInputPin("Condition", DataTypes.Bool)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Bool], 'outputs': [DataTypes.Bool]}

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self):
        data = self.condition.getData()
        if data:
            self.trueExec.call()
        else:
            self.falseExec.call()

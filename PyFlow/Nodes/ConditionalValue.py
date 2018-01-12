from AbstractGraph import *
from Settings import *
from Node import Node


class ConditionalValue(Node, NodeBase):
    def __init__(self, name, graph):
        super(ConditionalValue, self).__init__(name, graph)
        self.condition = self.addInputPin('condition', DataTypes.Bool)
        self.trueValue = self.addInputPin('ifTrue', DataTypes.Any)
        self.falseValue = self.addInputPin('ifFalse', DataTypes.Any)
        self.output = self.addOutputPin('out', DataTypes.Any)
        pinAffects(self.condition, self.output)
        pinAffects(self.trueValue, self.output)
        pinAffects(self.falseValue, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Bool, DataTypes.Any], 'outputs': [DataTypes.Any]}

    @staticmethod
    def category():
        return 'FlowControl'

    def compute(self):

        condition = self.condition.getData()
        tVal = self.trueValue.getData()
        fVal = self.falseValue.getData()
        try:
            if condition:
                self.output.setData(tVal)
            else:
                self.output.setData(fVal)
        except Exception, e:
            print e

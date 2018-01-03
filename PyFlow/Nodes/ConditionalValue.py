from AbstractGraph import *
from Settings import *
from Node import Node


class ConditionalValue(Node, NodeBase):
    def __init__(self, name, graph):
        super(ConditionalValue, self).__init__(name, graph, spacings=Spacings)
        self.condition = self.addInputPin('condition', DataTypes.Bool)
        self.trueValue = self.addInputPin('ifTrue', DataTypes.Any)
        self.falseValue = self.addInputPin('ifFalse', DataTypes.Any)
        self.output = self.addOutputPin('out', DataTypes.Any)
        portAffects(self.condition, self.output)
        portAffects(self.trueValue, self.output)
        portAffects(self.falseValue, self.output)

    @staticmethod
    def inputPinsTypes():
        return [DataTypes.Bool, DataTypes.Any]

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

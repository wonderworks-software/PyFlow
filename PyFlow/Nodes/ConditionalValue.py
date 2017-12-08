from AbstractGraph import *
from Settings import *
from Node import Node


class ConditionalValue(Node, NodeBase):
    def __init__(self, name, graph):
        super(ConditionalValue, self).__init__(name, graph, spacings=Spacings)
        self.condition = self.add_input_port('condition', DataTypes.Bool)
        self.trueValue = self.add_input_port('ifTrue', DataTypes.Any)
        self.falseValue = self.add_input_port('ifFalse', DataTypes.Any)
        self.output = self.add_output_port('out', DataTypes.Any)
        portAffects(self.condition, self.output)
        portAffects(self.trueValue, self.output)
        portAffects(self.falseValue, self.output)

    @staticmethod
    def get_category():
        return 'FlowControl'

    def compute(self):

        condition = self.condition.get_data()
        tVal = self.trueValue.get_data()
        fVal = self.falseValue.get_data()
        try:
            if condition:
                self.output.set_data(tVal)
            else:
                self.output.set_data(fVal)
        except Exception, e:
            print e

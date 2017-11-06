from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ConditionalValue(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ConditionalValue, self).__init__(name, graph, spacings=Spacings)
        self.condition = self.add_input_port('condition', AGPortDataTypes.tBool)
        self.trueValue = self.add_input_port('ifTrue', AGPortDataTypes.tAny)
        self.falseValue = self.add_input_port('ifFalse', AGPortDataTypes.tAny)
        self.output = self.add_output_port('out', AGPortDataTypes.tAny)
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
                self.output.set_data(tVal, False)
            else:
                self.output.set_data(fVal, False)
        except Exception, e:
            print e

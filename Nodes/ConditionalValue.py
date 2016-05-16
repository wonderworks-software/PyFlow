from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ConditionalValue(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ConditionalValue, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.graph = graph
        self.condition = self.add_input_port('condition', AGPortDataTypes.tBool)
        self.trueValue = self.add_input_port('ifTrue', AGPortDataTypes.tAny)
        self.falseValue = self.add_input_port('ifFalse', AGPortDataTypes.tAny)
        self.output = self.add_output_port('out', AGPortDataTypes.tAny)
        portAffects(self.condition, self.output)
        portAffects(self.trueValue, self.output)
        portAffects(self.falseValue, self.output)

    def compute(self):

        condition = self.condition.get_data()
        tVal = self.trueValue.get_data()
        fVal = self.falseValue.get_data()
        try:
            if condition:
                self.output.set_data(tVal, True)
            else:
                self.output.set_data(fVal, True)
        except Exception, e:
            print e

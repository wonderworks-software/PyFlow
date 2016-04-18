from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ArrayAppend(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ArrayAppend, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_arr = self.add_input_port('in array', AGPortDataTypes.tAny)
        self.element = self.add_input_port('element', AGPortDataTypes.tAny)
        self.out_arr = self.add_output_port('out', AGPortDataTypes.tAny)
        self.out_result = self.add_output_port('result', AGPortDataTypes.tBool)
        portAffects(self.in_arr, self.out_result)
        portAffects(self.element, self.out_result)
        portAffects(self.in_arr, self.out_arr)
        portAffects(self.element, self.out_arr)

    def compute(self):

        in_arr = self.in_arr.get_data()
        element = self.element.get_data()
        try:
            in_arr.append(element)
            self.out_arr.set_data(in_arr, False)
            self.out_result.set_data(True, False)
        except Exception, e:
            self.out_result.set_data(False, False)
            print e

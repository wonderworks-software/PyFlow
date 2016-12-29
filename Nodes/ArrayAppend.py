from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class ArrayAppend(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(ArrayAppend, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_arr = self.add_input_port('inArray', AGPortDataTypes.tArray)
        self.element = self.add_input_port('element', AGPortDataTypes.tAny)
        self.out_arr = self.add_output_port('out', AGPortDataTypes.tArray)
        self.out_result = self.add_output_port('result', AGPortDataTypes.tBool)
        portAffects(self.in_arr, self.out_result)
        portAffects(self.element, self.out_result)
        portAffects(self.in_arr, self.out_arr)
        portAffects(self.element, self.out_arr)

    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):

        try:
            in_arr = self.in_arr.get_data()
            element = self.element.get_data()
            out_arr = [] + in_arr
            del in_arr[:]
            del in_arr
            out_arr.append(element)
            self.out_arr.set_data(out_arr, False)
            self.out_result.set_data(True, False)
        except Exception, e:
            self.out_result.set_data(False, False)
            print e

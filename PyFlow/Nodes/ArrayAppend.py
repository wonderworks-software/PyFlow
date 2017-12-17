from AbstractGraph import *
from Settings import *
from Node import Node


class ArrayAppend(Node, NodeBase):
    def __init__(self, name, graph):
        super(ArrayAppend, self).__init__(name, graph, spacings=Spacings)
        self.in_arr = self.add_input_port('inArray', DataTypes.Array)
        self.element = self.add_input_port('element', DataTypes.Any)
        self.out_arr = self.add_output_port('out', DataTypes.Array)
        self.out_result = self.add_output_port('result', DataTypes.Bool)
        portAffects(self.in_arr, self.out_result)
        portAffects(self.element, self.out_result)
        portAffects(self.in_arr, self.out_arr)
        portAffects(self.element, self.out_arr)

    @staticmethod
    def category():
        return 'Array'

    def compute(self):

        try:
            in_arr = self.in_arr.get_data()
            element = self.element.get_data()
            out_arr = [] + in_arr
            del in_arr[:]
            del in_arr
            out_arr.append(element)
            self.out_arr.set_data(out_arr)
            self.out_result.set_data(True)
        except Exception as e:
            self.out_result.set_data(False)
            print(e)

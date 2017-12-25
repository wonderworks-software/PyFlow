from AbstractGraph import *
from Settings import *
from Node import Node


class ArrayAppend(Node, NodeBase):
    def __init__(self, name, graph):
        super(ArrayAppend, self).__init__(name, graph, spacings=Spacings)
        self.in_arr = self.addInputPin('inArray', DataTypes.Array)
        self.element = self.addInputPin('element', DataTypes.Any)
        self.out_arr = self.addOutputPin('out', DataTypes.Array)
        self.out_result = self.addOutputPin('result', DataTypes.Bool)
        portAffects(self.in_arr, self.out_result)
        portAffects(self.element, self.out_result)
        portAffects(self.in_arr, self.out_arr)
        portAffects(self.element, self.out_arr)

    @staticmethod
    def category():
        return 'Array'

    def compute(self):

        try:
            in_arr = self.in_arr.getData()
            element = self.element.getData()
            out_arr = [] + in_arr
            del in_arr[:]
            del in_arr
            out_arr.append(element)
            self.out_arr.setData(out_arr)
            self.out_result.setData(True)
        except Exception as e:
            self.out_result.setData(False)
            print(e)

from AbstractGraph import *
from Settings import *
from Node import Node


class Len(Node, NodeBase):
    def __init__(self, name, graph):
        super(Len, self).__init__(name, graph, spacings=Spacings)
        self.in_arr = self.addInputPin('iterable', DataTypes.Any)
        self.out_len = self.addOutputPin('len', DataTypes.Int)
        self.out_result = self.addOutputPin('result', DataTypes.Bool)
        pinAffects(self.in_arr, self.out_result)
        pinAffects(self.in_arr, self.out_len)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.Int, DataTypes.Bool]}

    @staticmethod
    def category():
        return 'Utils'

    def compute(self):

        in_arr = self.in_arr.getData()
        try:
            self.out_len.setData(len(in_arr))
            self.out_result.setData(True)
        except Exception, e:
            self.out_result.setData(False)
            print e

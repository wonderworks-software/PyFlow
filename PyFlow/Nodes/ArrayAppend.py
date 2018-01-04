from AbstractGraph import *
from Settings import *
from Node import Node


class ArrayAppend(Node, NodeBase):
    def __init__(self, name, graph):
        super(ArrayAppend, self).__init__(name, graph, spacings=Spacings)
        self.inExec = self.addInputPin('execIn', DataTypes.Exec, self.compute, True)
        self.outExec = self.addOutputPin('execOut', DataTypes.Exec, None, True)

        self.in_arr = self.addInputPin('inArray', DataTypes.Array)
        self.element = self.addInputPin('element', DataTypes.Any)

        self.newItemIndex = self.addOutputPin('out', DataTypes.Int)
        self.out_result = self.addOutputPin('result', DataTypes.Bool)

        pinAffects(self.in_arr, self.newItemIndex)
        pinAffects(self.in_arr, self.out_result)

        pinAffects(self.element, self.newItemIndex)
        pinAffects(self.element, self.out_result)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Exec, DataTypes.Array, DataTypes.Any],
                'outputs': [DataTypes.Exec, DataTypes.Int, DataTypes.Bool]}

    @staticmethod
    def description():
        return '''Appends element to array.'''

    @staticmethod
    def category():
        return 'Array'

    def compute(self):
        try:
            element = self.element.getData()
            if len(self.in_arr.edge_list) == 0:
                self.newItemIndex.setClean()
                self.out_result.setClean()
                self.outExec.call()
                return
            in_arr = self.in_arr.getData()
            in_arr.append(element)
            self.newItemIndex.setData(len(in_arr) - 1)
            self.out_result.setData(True)

        except Exception as e:
            self.out_result.setData(False)
            print(e)
        self.outExec.call()

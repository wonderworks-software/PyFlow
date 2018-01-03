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

        portAffects(self.in_arr, self.newItemIndex)
        portAffects(self.in_arr, self.out_result)

        portAffects(self.element, self.newItemIndex)
        portAffects(self.element, self.out_result)

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

            in_arr = self.in_arr.getData()
            in_arr.append(element)
            self.newItemIndex.setData(in_arr.index(element))
            self.out_result.setData(True)
        except Exception as e:
            self.out_result.setData(False)
            print(e)
        self.outExec.call()

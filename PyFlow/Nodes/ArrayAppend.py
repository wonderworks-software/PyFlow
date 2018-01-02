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
        self.out_arr = self.addOutputPin('out', DataTypes.Array)
        self.out_result = self.addOutputPin('result', DataTypes.Bool)
        self.bGetRef = self.addInputPin('get ref?', DataTypes.Bool)

        portAffects(self.in_arr, self.out_result)
        portAffects(self.element, self.out_result)
        portAffects(self.in_arr, self.out_arr)
        portAffects(self.element, self.out_arr)

    @staticmethod
    def description():
        return '''Appends element to array. If 'get ref?' is set to False - copy of array will be taken.'''

    @staticmethod
    def category():
        return 'Array'

    def compute(self):
        try:
            element = self.element.getData()

            # array is mutable type
            # choose how to get it - copy or reference
            bGetRef = self.bGetRef.getData()
            if bGetRef:
                in_arr = self.in_arr.getData()
            else:
                in_arr = list(self.in_arr.getData())
            in_arr.append(element)
            self.out_arr.setData(in_arr)
            self.out_result.setData(True)
        except Exception as e:
            self.out_result.setData(False)
            print(e)
        self.outExec.call()

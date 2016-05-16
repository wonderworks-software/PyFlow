from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class IsArray(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(IsArray, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp = self.add_input_port('obj', AGPortDataTypes.tAny)
        self.out = self.add_output_port('out', AGPortDataTypes.tBool)
        portAffects(self.inp, self.out)

    def compute(self):

        data = self.inp.get_data()
        result = False
        try:
            len(data)
            result = True
        except Exception, e:
            result = False
            self.graph.write_to_console("[ERROR] {0}. {1}".format(self.__class__.__name__, e))
        self.out.set_data(result, True)

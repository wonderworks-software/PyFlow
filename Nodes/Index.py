from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


class Index(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Index, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inArray = self.add_input_port('iterable', AGPortDataTypes.tAny)
        self.value = self.add_input_port('value', AGPortDataTypes.tAny)
        self.index = self.add_output_port('idx', AGPortDataTypes.tNumeric)
        self.success = self.add_output_port('success', AGPortDataTypes.tBool)
        portAffects(self.inArray, self.index)
        portAffects(self.value, self.index)

    def compute(self):

        ls = self.inArray.get_data()
        value = self.value.get_data()
        try:
            idx = ls.index(value)
            self.index.set_data(int(idx), True)
            self.success.set_data(True)
        except Exception, e:
            self.success.set_data(False)
            self.graph.write_to_console("[ERROR] {0}. {1}".format(self.__class__.__name__, e))

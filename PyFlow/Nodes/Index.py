from AbstractGraph import *
from Settings import *
from Node import Node


class Index(Node, NodeBase):
    def __init__(self, name, graph):
        super(Index, self).__init__(name, graph, spacings=Spacings)
        self.inArray = self.add_input_port('iterable', DataTypes.Any)
        self.value = self.add_input_port('value', DataTypes.Any)
        self.index = self.add_output_port('idx', DataTypes.Float)
        self.success = self.add_output_port('success', DataTypes.Bool)
        portAffects(self.inArray, self.index)
        portAffects(self.value, self.index)

    @staticmethod
    def get_category():
        return 'Array'

    def compute(self):

        ls = self.inArray.get_data()
        value = self.value.get_data()
        try:
            idx = ls.index(value)
            self.index.set_data(int(idx))
            self.success.set_data(True)
        except Exception, e:
            self.success.set_data(False)
            self.graph.write_to_console("[ERROR] {0}. {1}".format(self.__class__.__name__, e))

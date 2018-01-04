from Node import Node
from Settings import *
from AbstractGraph import *


class StringReplace(Node, NodeBase):
    def __init__(self, name, graph):
        super(StringReplace, self).__init__(name, graph, spacings=Spacings)
        self.first = self.addInputPin('source', DataTypes.String)
        self.old_ptn = self.addInputPin('old pattern', DataTypes.String)
        self.new_ptn = self.addInputPin('new pattern', DataTypes.String)
        self.output = self.addOutputPin('output', DataTypes.String)
        pinAffects(self.first, self.output)
        pinAffects(self.old_ptn, self.output)
        pinAffects(self.new_ptn, self.output)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.String]}

    @staticmethod
    def category():
        return 'String'

    def compute(self):

        first_str = self.first.getData()
        old_ptn = self.old_ptn.getData()
        new_ptn = self.new_ptn.getData()
        try:
            result = first_str.replace(old_ptn, new_ptn)
            self.output.setData(result)
        except Exception, e:
            print e

from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class ToString(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(ToString, self).__init__(name, graph)
        self.in_data = self.addInputPin('in', DataTypes.Any, hideLabel=True, bCreateInputWidget=False)
        self.out_data = self.addOutputPin('out', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.in_data, self.out_data)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.Any], 'outputs': [DataTypes.String]}

    @staticmethod
    def category():
        return 'Convert'

    def compute(self):

        out_data = self.in_data.getData()
        try:
            self.out_data.setData(str(out_data))
        except Exception, e:
            print e

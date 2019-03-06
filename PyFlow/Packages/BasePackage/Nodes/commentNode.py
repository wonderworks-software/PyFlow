from PyFlow.Core import NodeBase


class commentNode(NodeBase):
    def __init__(self, name):
        super(commentNode, self).__init__(name)

    @staticmethod
    def category():
        return 'Common'

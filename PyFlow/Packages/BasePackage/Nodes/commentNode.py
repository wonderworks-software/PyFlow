from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import NodeBase


## If else node
class commentNode(NodeBase):
    def __init__(self, name):
        super(commentNode, self).__init__(name)

    @staticmethod
    def category():
        return 'Common'
